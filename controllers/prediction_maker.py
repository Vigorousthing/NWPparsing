from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.MongoDbConnector import *
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.input_converter import InputConverter
import keras
import CONSTANT
import numpy as np
import pandas as pd
import datetime


class PredictionMaker:
    def __init__(self, file_type, fold_type, location,
                 variables, model_name):
        self.analyzer = NwpGridAnalyzer()
        self.visualizer = Visualizer()
        self.container = FilesContainer(file_type, fold_type,
                                        location, variables)
        self.ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id,
                                        CONSTANT.ftp_pw)
        self.input_converter = InputConverter()

        self.master = DataOrganizer(self.analyzer, self.container)
        self.prediction_model = keras.models.load_model(
            CONSTANT.model_path + model_name)

    def download_and_container_set(self):
        raise NotImplementedError

    def extract_base_data(self):
        raise NotImplementedError

    def make_prediction(self, nwp_df):
        raise NotImplementedError

    def make_prediction_df(self, nwp_df, prediction_array):
        raise NotImplementedError

    def merge_with_siteinfo(self, prediction_df):
        raise NotImplementedError

    def amend_for_final_result(self):
        pass


class RealTimePredictionMaker(PredictionMaker):
    def __init__(self, file_type, fold_type, location, variables, model_name):
        super(RealTimePredictionMaker, self).__init__(
            file_type, fold_type, location, variables, model_name)

    def create_realtime_prediction(self):
        self.download_and_container_set()
        df = self.extract_base_data(remove=False)
        prediction = self.make_prediction(df)
        prediction_df = self.make_prediction_df(df, prediction)
        result = self.prediction_df_pipeline_to_result(prediction_df)
        return result

    def prediction_df_pipeline_to_result(self, prediction_df):
        result = self.merge_with_siteinfo(prediction_df)
        result = self.apply_capacity_to_prediction(result)
        result = self.amend_time_columns(result)
        result = self.amend_etc(result)
        return result

    def download_and_container_set(self):
        self.container.generate_real_time_prediction_files(self.ftp_accessor)
        self.ftp_accessor.download_files(self.container.filename_list,
                                         self.container.type.nwp_type)

    def extract_base_data(self, remove=True):
        df = self.master.data_collect(CONSTANT.num_of_process)
        if df is None:
            return "nothing to show. something was gone wrong"
        # remove after a prediction is successfully made
        if remove is True:
            self.ftp_accessor.remove_from_local_pc(self.container.filename_list)
        return df

    def make_prediction(self, nwp_df):
        prediction_df = nwp_df.drop(
            columns=CONSTANT.subtract_for_prediction_df)
        return self.prediction_model.predict(np.array(prediction_df))

    def make_prediction_df(self, nwp_df, prediction_array):
        nwp_df["prediction"] = prediction_array
        return nwp_df

    def merge_with_siteinfo(self, prediction_df):
        site_info_df = get_site_info_df().sort_values(by=["COMPX_ID"],
                                                      ascending=True)
        prediction_df = prediction_df.sort_values(
            by=["location_num"], ascending=True)
        prediction_df = pd.merge(prediction_df, site_info_df, how="inner",
                                 on=["location_num"])
        return prediction_df

    @staticmethod
    def apply_capacity_to_prediction(df):
        df["capacity"] = pd.to_numeric(df["capacity"])
        df["FCST_QGEN"] = df.apply(
            lambda row: row.prediction * (row.capacity / 99), axis=1)
        return df

    @staticmethod
    def amend_time_columns(df):
        now_without_min_sec = datetime.datetime.now().replace(minute=0,
                                                              second=0,
                                                              microsecond=0)
        df["FCST_TM"] = df.apply(lambda row: row.FCST_TM.replace(
            minute=0, second=0, microsecond=0), axis=1)
        df["CRTN_TM"] = now_without_min_sec

        df["LEAD_HR"] = df.apply(
            lambda row: int(
                (row.FCST_TM - row.CRTN_TM).days * 24 +
                (row.FCST_TM - row.CRTN_TM).seconds / 3600
            ), axis=1)
        return df

    @staticmethod
    def amend_etc(df):
        result = df.rename(columns={"site": "COMPX_ID"})

        result = result.sort_values(by=["location_num", "FCST_TM"],
                                    ascending=True)
        result = result.drop(columns=["lat_x", "lat_y", "lon_x", "lon_y",
                                      "Coordinates", "prediction", "horizon",
                                      "location_num"])
        return result


class GeneralPredictionMaker(PredictionMaker):
    def __init__(self):
        super(GeneralPredictionMaker, self).__init__()

    def create_interval_prediction(self, prediction_type, model_name):
        converted_interval = self.input_converter.time_interval_conversion(
            self.time_info)
        start_time, end_time = self.container.time_alignment(
            converted_interval)
        current_time = start_time
        if prediction_type == "daily":
            time_step = 24
        else:
            time_step = 6

        # download hole prediction_list
        download_set = {None}
        while current_time <= end_time:
            self.container.generate_base_prediction_files(current_time)
            current_time += datetime.timedelta(hours=time_step)

        download_set = self.container.filename_list
        self.ftp_accessor.download_files(download_set,
                                         self.container.type.nwp_type)

        #
        self.container.initialize_except_output()
        current_time = start_time
        while current_time <= end_time:
            self.container.generate_base_prediction_files(current_time)
            current_time += datetime.timedelta(hours=time_step)
        df = self.master.data_collect(CONSTANT.num_of_process)

        if df is None:
            return "nothing to show. something was gone wrong"
        input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "lat", "lon"])
        model = keras.models.load_model(CONSTANT.model_path + model_name)
        prediction = model.predict(np.array(input_df))
        prediction_df = df.drop(columns=self.container.variables)