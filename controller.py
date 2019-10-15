from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.MongoDbConnector import *
from util.query_maker import *
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.QueueJobProgressIndicator import QueueJobProgressIndicator
from util.input_converter import InputConverter
import keras
import time
import numpy as np
import pandas as pd
import datetime


class Controller:
    def __init__(self, file_type, fold_type, time_info, location, variables):
        self.time_info = time_info

        self.ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id,
                                        CONSTANT.ftp_pw)
        self.mongo_connector = MongodbConnector("sites", "production")

        self.analyzer = NwpGridAnalyzer()
        self.visualizer = Visualizer()
        self.container = FilesContainer(file_type, fold_type,
                                        location, variables)
        self.input_converter = InputConverter()
        self.queue_job_checker = None

        self.master = DataOrganizer(self.analyzer, self.container)

    def create_training_df(self, save_df_name):
        df = None
        converted_interval = self.input_converter.time_interval_conversion(
            self.time_info)
        time_interval_list = self.split_time(converted_interval)

        for i, time_interval in enumerate(time_interval_list):
            self.container.initialize_except_output()
            self.container.generate_base_files(time_interval)

            if not self.ftp_accessor.check_connection():
                self.ftp_accessor.reconnect()

            self.ftp_accessor.download_files(self.container.filename_list,
                                             self.container.type.nwp_type)

            self.queue_job_checker = QueueJobProgressIndicator(
                self.container.container)
            self.queue_job_checker.start()
            start = time.time()
            temp_df = self.master.data_collect(CONSTANT.num_of_process)
            temp_df.to_excel(
                CONSTANT.data_file_path + "temp_file_" + str(i) +
                ".xlsx")
            if i == 0:
                df = temp_df
            else:
                df = df.append(temp_df)

            end = time.time()
            # self.ftp_accessor.remove_from_local_pc(filename_list)
            print("passed in {}th iteration : ".format(i), end - start)
            self.queue_job_checker.terminate()
        df.to_excel(CONSTANT.data_file_path + "{}.xlsx".
                    format(save_df_name))

    def create_training_df_from_files_in_directory(self, path):
        self.container.create_training_data_files_from_directory(path)
        self.queue_job_checker = QueueJobProgressIndicator(
            self.container.container)
        self.queue_job_checker.start()
        df = self.master.data_collect(CONSTANT.num_of_process)
        # df.to_excel(
        #     CONSTANT.data_file_path + "temp_file_" + str(i) +
        #     ".xlsx")
        self.queue_job_checker.terminate()
        return df

    def create_current_predcition(self, model_name):
        current_time = self.input_converter.current_time_conversion(
            self.time_info)
        self.container.generate_base_prediction_files(current_time)
        filename_list = self.container.filename_list

        if not self.ftp_accessor.check_connection():
            self.ftp_accessor.reconnect()

        self.ftp_accessor.download_files(filename_list,
                                         self.container.type.nwp_type)

        progress_check = QueueJobProgressIndicator(self.container.container)
        progress_check.start()

        df = self.master.data_collect(CONSTANT.num_of_process)
        input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "Coordinates"])
        prediction_df = df.drop(columns=self.container.variables)

        model = keras.models.load_model(CONSTANT.model_path + model_name)
        prediction = model.predict(np.array(input_df))

        return self.amend_prediction_df(prediction_df, prediction,
                                        self.time_info)

    def create_realtime_prediction(self, model_name):
        self.container.generate_real_time_prediction_files(self.ftp_accessor)
        self.ftp_accessor.download_files(self.container.filename_list,
                                         self.container.type.nwp_type)
        df = self.master.data_collect(CONSTANT.num_of_process)
        if df is None:
            return "nothing to show. something was gone wrong"
        input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "lat", "lon"])
        model = keras.models.load_model(CONSTANT.model_path + model_name)
        prediction = model.predict(np.array(input_df))

        prediction_df = df.drop(columns=self.container.variables)

        # remove after a prediction is successfully made
        self.ftp_accessor.remove_from_local_pc(self.container.filename_list)
        result = self.amend_prediction_df(prediction_df, prediction,
                                          self.time_info)
        result["Coordinates"] = result.apply(
            lambda row: (float(row.lat), float(row.lon)), axis=1)

        site_info_df = get_site_info_df()

        result = pd.merge(result, site_info_df, how="inner",
                          on=["Coordinates"])
        result["capacity"] = pd.to_numeric(result["capacity"])
        result["FCST_QGEN"] = result.apply(
            lambda row: row.prediction*(row.capacity/99), axis=1)
        result = result.rename(columns={"site": "COMPX_ID"})
        result = result.drop(columns=["lat_x", "lat_y", "lon_x", "lon_y",
                                      "Coordinates", "prediction",
                                      "location_num"])
        now_without_min_sec = datetime.datetime.now().replace(minute=0,
                                                              second=0,
                                                              microsecond=0)
        result["FCST_TM"] = result.apply(lambda row: row.FCST_TM.replace(
            minute=0, second=0, microsecond=0), axis=1)
        result["CRTN_TM"] = now_without_min_sec

        result["LEAD_HR"] = result.apply(
            lambda row: int(
                        (row.FCST_TM - row.CRTN_TM).days * 24 +
                        (row.FCST_TM - row.CRTN_TM).seconds / 3600
                        ), axis=1)

        result = result.sort_values(by=["COMPX_ID", "FCST_TM"],
                                    ascending=True)
        return result

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

        # download
        download_set = {None}
        while current_time <= end_time:
            self.container.generate_base_prediction_files(current_time)
            current_time += datetime.timedelta(hours=time_step)

        download_set = self.container.filename_list
        self.ftp_accessor.download_files(download_set,
                                         self.container.type.nwp_type)

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

        return self.amend_prediction_df(prediction_df, prediction,
                                        self.time_info)

    def amend_prediction_df(self, prediction_df, prediction, current_time):
        # prediction_df["CRTN_TM"] = \
        #     self.input_converter.current_time_conversion(current_time)
        prediction_df = prediction_df.drop(columns=["horizon"])
        # prediction_df["new_horizon"] = prediction_df.apply(
        #     lambda row: int(
        #                 (row.FCST_TM - row.CRTN_TM).days * 24 +
        #                 (row.FCST_TM - row.CRTN_TM).seconds / 3600
        #                 ),
        #                 axis=1)
        prediction_df["prediction"] = prediction
        return prediction_df

    def create_real_vpp(self, time_interval, plant_id_list):
        location_num_table = pd.DataFrame(
            list(zip(plant_id_list, [i for i in range(len(plant_id_list))])),
            columns=["COMPX_ID", "location_num"])

        mongo_connector = MongodbConnector("sites", "production")
        mongo_connector2 = MongodbConnector("sites", "sitesList")
        query = vpp_production_query(time_interval,
                                     match_plant_subquery(plant_id_list))

        real_df = mongo_connector.aggregate(query)
        site_info_df = get_sitelist(mongo_connector2.find_latest())

        real_df = real_df.drop(columns=["_id"])
        site_info_df = site_info_df.rename(columns={"site": "COMPX_ID"})
        site_info_df = pd.merge(site_info_df, location_num_table, how="left",
                                on=["COMPX_ID"])

        merged = pd.merge(real_df, site_info_df, how="left", on=["COMPX_ID"])
        merged = merged.rename(columns={"CRTN_TM": "FCST_TM"})
        merged = merged.rename(columns={"lng": "lon"})

        return merged

    def create_real_jenon(self, time_interval):

        pass

    @staticmethod
    def split_time(converted_time_interval):
        time_interval_list = []
        start, end = converted_time_interval[0], converted_time_interval[1]
        temp_list = []
        while start <= end:
            temp_list.append(start)
            start += datetime.timedelta(days=
                                        CONSTANT.
                                        length_of_time_interval_for_training)
            start -= datetime.timedelta(hours=1)
            if start <= end:
                temp_list.append(start)
                start += datetime.timedelta(hours=1)
            else:
                temp_list.append(end)
            time_interval_list.append(temp_list)
            temp_list = []
        return time_interval_list


def merge_two_dfs(join_key_list, df1, df2):
    joined_df = pd.merge(left=df1, right=df2,
                         how="left", on=join_key_list)
    joined_df = joined_df.fillna(0)
    return joined_df




