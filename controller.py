from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.MongoDbConnector import *
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
            self.container.generate_base_files(time_interval)

            filename_list = self.container.filename_list
            if not self.ftp_accessor.check_connection():
                self.ftp_accessor.reconnect()
            self.ftp_accessor.download_files(filename_list,
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
            self.ftp_accessor.remove_from_local_pc(filename_list)
            self.container.initialize_filename_list()
            print("passed in {}th iteration : ".format(i), end - start)
            self.queue_job_checker.terminate()
        df.to_excel(CONSTANT.data_file_path + "{}.xlsx".
                    format(save_df_name))

    def create_training_df_sunghun_test(self, path):
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
        prediction_df = df.drop(columns=self.container.variables)

        model = keras.models.load_model(CONSTANT.model_path + model_name)
        prediction = model.predict(np.array(input_df))

        return self.amend_prediction_df(prediction_df, prediction,
                                        self.time_info)

    def amend_prediction_df(self, prediction_df, prediction, current_time):
        prediction_df["CRTN_TM"] = \
            self.input_converter.current_time_conversion(current_time)
        prediction_df["new_horizon"] = prediction_df.apply(
            lambda row: int(
                        (row.FCST_TM - row.CRTN_TM).days * 24 +
                        (row.FCST_TM - row.CRTN_TM).seconds / 3600
                        ),
                        axis=1)
        prediction_df["prediction"] = prediction
        prediction_df = prediction_df.drop(columns=["horizon"])
        return prediction_df

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


def create_interval_prediction(container, ftp_accessor, time_interval,
                               prediction_type):
    start_time, end_time = container.time_alignment(time_interval)
    current_time = start_time
    if prediction_type == "daily":
        time_step = 24
    else:
        time_step = 6

    # download
    download_set = {None}
    while current_time <= end_time:
        container.generate_base_prediction_files(current_time)
        download_set.union(set(container.filname_list))
        current_time += datetime.timedelta(hours=time_step)
    ftp_accessor.download_files(download_set, container.type.nwp_type)

    current_time = start_time
    while current_time <= end_time:

        container.generate_base_prediction_files(current_time)
        download_set.union(set(container.filname_list))
        current_time += datetime.timedelta(hours=time_step)

