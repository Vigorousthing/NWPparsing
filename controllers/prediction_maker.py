from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.MongoDbConnector import *
from nwp_object.NwpFile import *
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.input_converter import InputConverter
import keras
import CONSTANT
import numpy as np
import pandas as pd
import datetime
import time


class PredictionMaker:
    def __init__(self, fold_type, location,
                 ldaps_model_name, rdaps_model_name):
        self.input_converter = InputConverter()
        self.analyzer = NwpGridAnalyzer()
        self.visualizer = Visualizer()

        self.ldaps_variables = self.var_from_model_name(ldaps_model_name)
        self.rdaps_variables = self.var_from_model_name(rdaps_model_name)

        self.ldaps_container = FilesContainer(LdapsFile, fold_type,
                                              location, self.ldaps_variables)
        self.rdaps_container = FilesContainer(RdapsFile, fold_type,
                                              location, self.rdaps_variables)
        self.ldaps_prediction_model = keras.models.load_model(
            CONSTANT.model_path + ldaps_model_name)
        self.rdaps_prediction_model = keras.models.load_model(
            CONSTANT.model_path + rdaps_model_name)

        self.ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id,
                                        CONSTANT.ftp_pw)
        self.master = DataOrganizer(self.analyzer, self.ldaps_container)

    def create_prediction(self):
        raise NotImplementedError

    def download_and_container_set(self, container):
        raise NotImplementedError

    def extract_base_data(self, container, remove=True):
        raise NotImplementedError

    def make_prediction(self, nwp_df, prediction_model):
        raise NotImplementedError

    def merge_with_siteinfo(self, prediction_df):
        raise NotImplementedError

    @staticmethod
    def var_from_model_name(model_name):
        df = pd.read_excel(CONSTANT.setting_file_path +
                           CONSTANT.var_by_model_file_name)
        return df[model_name][0].replace(" ", "").split(",")


class RealTimePredictionMakerForAllVpp(PredictionMaker):
    def __init__(self, fold_type, location,
                 ldaps_model_name, rdaps_model_name):
        super(RealTimePredictionMakerForAllVpp, self).__init__(
            fold_type, location, ldaps_model_name, rdaps_model_name)
        self.current_time = datetime.datetime.now().replace(
            minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)

    def create_prediction(self, remove=True):
        self.download_and_container_set(self.ldaps_container)
        ldaps_df = self.extract_base_data(self.ldaps_container, remove=remove)
        prediction = self.make_prediction(
            ldaps_df, self.ldaps_prediction_model)
        prediction_df = self.make_prediction_df_ldaps(ldaps_df, prediction)
        ldaps_result = self.prediction_df_pipeline_to_result(prediction_df)

        self.download_and_container_set(self.rdaps_container)
        self.master.reset_container(self.rdaps_container)
        rdaps_df = self.extract_base_data(self.rdaps_container, remove=remove)
        prediction = self.make_prediction(
            rdaps_df, self.rdaps_prediction_model)
        prediction_df = self.make_prediction_df_rdaps(rdaps_df, prediction)
        rdaps_result = self.prediction_df_pipeline_to_result(prediction_df)
        rdaps_result = rdaps_result[rdaps_result.LEAD_HR.isin(
            self.ldaps_container.lead_hr_failed)]
        return ldaps_result, rdaps_result

    def prediction_df_pipeline_to_result(self, prediction_df):
        result = self.merge_with_siteinfo(prediction_df)
        result = self.apply_capacity_to_prediction(result)
        result = self.amend_time_columns(result)
        result = self.amend_etc(result)
        return result

    def download_and_container_set(self, container):
        container.generate_real_time_prediction_files(
            self.ftp_accessor, self.current_time)
        self.ftp_accessor.download_files(container.filename_list,
                                         container.type.nwp_type)

    def extract_base_data(self, container, remove=True):
        df = self.master.data_collect(CONSTANT.num_of_process)
        if df is None:
            return "nothing to show. something was gone wrong"
        # remove after a prediction is successfully made
        if remove is True:
            self.ftp_accessor.remove_from_local_pc(
                container.filename_list)
        return df

    def make_prediction(self, nwp_df, prediction_model):
        prediction_df = nwp_df.drop(
            columns=CONSTANT.subtract_for_prediction_df)
        return prediction_model.predict(np.array(prediction_df))

    @staticmethod
    def make_prediction_df_ldaps(nwp_df, prediction_array):
        nwp_df["prediction"] = prediction_array
        return nwp_df

    @staticmethod
    def make_prediction_df_rdaps(nwp_df, prediction_array):
        # df = nwp_df.drop(columns=self.rdaps_container.variables)
        df = nwp_df
        df.reset_index(drop=True, inplace=True)

        num = 0
        dic = {}
        col = ["CRTN_TM", "horizon", "FCST_TM", "lat", "lon",
               "location_num", "prediction"]
        for idx in range(df.shape[0]):
            df.at[idx, "prediction"] = prediction_array[idx][2]

            crtn_tm = df.at[idx, "CRTN_TM"]
            lat = df.at[idx, "lat"]
            lon = df.at[idx, "lon"]
            location_num = df.at[idx, "location_num"]
            for i in range(2):
                new_horizon = df.at[idx, "horizon"] - (i + 1)
                new_fcst_tm = df.at[idx, "FCST_TM"] - datetime.timedelta(
                    hours=i + 1)
                n_row = (crtn_tm, new_horizon, new_fcst_tm, lat, lon,
                         location_num, prediction_array[idx][1 - i])
                dic[num] = n_row
                num += 1

        n_df = pd.DataFrame.from_dict(dic, orient="index", columns=col)

        df = df.append(n_df, sort=False)
        df.reset_index(drop=True, inplace=True)
        return df

    def merge_with_siteinfo(self, prediction_df):
        site_info_df = get_site_info_df()
        site_info_df["location_num"] = [i for i in range(len(site_info_df))]
        site_info_df = site_info_df.sort_values(by=["COMPX_ID"],
                                                ascending=True)

        prediction_df = prediction_df.sort_values(
            by=["location_num"], ascending=True)
        prediction_df = pd.merge(prediction_df, site_info_df, how="inner",
                                 on=["location_num"])
        return prediction_df

    def amend_time_columns(self, df):
        # should be amended
        df["FCST_TM"] = df.apply(lambda row: row.FCST_TM.replace(
            minute=0, second=0, microsecond=0), axis=1)
        df["CRTN_TM"] = self.current_time

        df["LEAD_HR"] = df.apply(
            lambda row: int(
                (row.FCST_TM - row.CRTN_TM).days * 24 +
                (row.FCST_TM - row.CRTN_TM).seconds / 3600
            ), axis=1)
        return df

    @staticmethod
    def apply_capacity_to_prediction(df):
        df["capacity"] = pd.to_numeric(df["capacity"])
        df["FCST_QGEN"] = df.apply(
            lambda row: row.prediction * (row.capacity / 99), axis=1)
        return df

    @staticmethod
    def amend_etc(df):
        result = df.rename(columns={"site": "COMPX_ID"})

        result = result.sort_values(by=["location_num", "FCST_TM"],
                                    ascending=True)
        result = result.drop(columns=["lat_x", "lat_y", "lon_x", "lon_y",
                                      "Coordinates", "prediction", "horizon",
                                      "location_num"])
        result["FCST_QGEN"][result["FCST_QGEN"] < 1] = 0
        return result


class TimeDesignatedPredictionMaker(RealTimePredictionMakerForAllVpp):
    def __init__(self, fold_type, location,
                 ldaps_model_name, rdaps_model_name, designated_time):
        super(TimeDesignatedPredictionMaker, self).__init__(fold_type,
                                                            location,
                                                            ldaps_model_name,
                                                            rdaps_model_name)
        self.designated_time = designated_time

    def download_and_container_set(self, container):
        container.generate_base_prediction_files(self.designated_time)
        self.ftp_accessor.download_files(container.filename_list,
                                         container.type.nwp_type)

    def amend_time_columns(self, df):
        df["FCST_TM"] = df.apply(lambda row: row.FCST_TM.replace(
            minute=0, second=0, microsecond=0), axis=1)
        df["CRTN_TM"] = self.designated_time.replace(minute=0)

        df["LEAD_HR"] = df.apply(
            lambda row: int(
                (row.FCST_TM - row.CRTN_TM).days * 24 +
                (row.FCST_TM - row.CRTN_TM).seconds / 3600
            ), axis=1)
        return df


class GeneralPredictionMaker(RealTimePredictionMakerForAllVpp):
    def __init__(self, fold_type, location, ldaps_model_name,
                 rdaps_model_name):
        super(GeneralPredictionMaker, self).__init__(fold_type, location,
                                                     ldaps_model_name,
                                                     rdaps_model_name)

    def create_interval_prediction(self, prediction_type, time_interval):
        start_time, end_time = self.input_converter.time_interval_conversion(
            time_interval)
        time_adjustment = (start_time - datetime.timedelta(hours=9)).hour % 6
        start_time = start_time - datetime.timedelta(hours=time_adjustment)

        current_time = start_time
        if prediction_type == "daily":
            time_step = 24
        else:
            time_step = 6

        # make whole
        while current_time <= end_time:
            self.ldaps_container.generate_base_prediction_files(current_time)
            current_time += datetime.timedelta(hours=time_step)

        # download whole prediction_list
        download_set = self.ldaps_container.filename_list
        self.ftp_accessor.download_files(download_set,
                                         self.ldaps_container.type.nwp_type)

        # extract nwp data
        # self.ldaps_container.initialize_except_output()
        df = self.master.data_collect(CONSTANT.num_of_process)
        if df is None:
            return "nothing to show. something was gone wrong"

        # while current_time <= end_time:
        #     self.ldaps_container.generate_base_prediction_files(current_time)
        #     df = self.master.data_collect(CONSTANT.num_of_process)
        #
        #     current_time += datetime.timedelta(hours=time_step)
        #     self.ldaps_container.initialize_except_output()

        # 1. make prediction  2. prediction df
        input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "lat", "lon",
                                    "location_num", "horizon"])
        prediction = self.ldaps_prediction_model.predict(np.array(input_df))
        # prediction_df = df.drop(columns=self.ldaps_container.variables)
        df["prediction"] = prediction
        return df

    def create_prediction(self, remove=True):
        self.download_and_container_set(self.ldaps_container)
        ldaps_df = self.extract_base_data(self.ldaps_container, remove=remove)
        prediction = self.make_prediction(
            ldaps_df, self.ldaps_prediction_model)
        prediction_df = self.make_prediction_df_ldaps(ldaps_df, prediction)
        return self.prediction_df_pipeline_to_result(prediction_df)
