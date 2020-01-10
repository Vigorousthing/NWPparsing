from controllers.prediction_maker import GeneralPredictionMaker
from data_accessors.MongoDbConnector import get_site_info_df
from util.input_converter import InputConverter
from controllers.real_data_maker import VppRealMaker, JenonRealMaker
import pandas as pd
import numpy as np
import math
import CONSTANT


class GeneralEval:
    def __init__(self, time_interval):
        self.time_interval = time_interval
        self.merged = None

        self.prediction_maker = None
        self.real_maker = None

    def create_data_and_merge(self):
        raise NotImplementedError

    def make_criteria_column_and_groupby_horizon(self):
        self.merged["rmse"] = (self.merged["production"] - self.merged["prediction"]) ** 2
        self.merged["mape"] = abs(self.merged["production"] - self.merged["prediction"])
        self.merged["mbe"] = self.merged["production"] - self.merged["prediction"]

        self.merged = self.merged.groupby(self.merged["horizon"])
        self.merged = self.merged.agg(["count", "mean", "sum"])

    def cal_final_criteria(self):
        self.merged["rRMSE"] = (self.merged["rmse"]["sum"].apply(np.sqrt)) / (self.merged[
                                                                        "production"][
                                                                        "mean"] *
                                                                    self.merged[
                                                                        "production"][
                                                                        "count"].apply(
                                                                        np.sqrt))
        self.merged["rMBE"] = self.merged["mbe"]["sum"] / (self.merged["production"]["mean"] *
                                                 self.merged["production"]["count"])

    def make_checkpoint(self, checkpoint_filename):
        self.merged.to_excel(CONSTANT.data_file_path + checkpoint_filename)

    def load_checkpoint(self, checkpoint_filename):
        self.merged = pd.read_excel(
            CONSTANT.data_file_path + checkpoint_filename)

    def save_output(self, output_filename):
        self.merged.to_excel(CONSTANT.data_file_path + output_filename)


class VppEval(GeneralEval):
    def __init__(self, time_interval, id_list):
        super(VppEval, self).__init__(time_interval)
        self.id_list = id_list
        self.setting = ["unis", InputConverter().vpp_compx_id_to_coordinates(
            id_list, get_site_info_df()), "nonje_1016model.h5", "rdaps.h5"]

    def make_connection(self):
        self.prediction_maker = GeneralPredictionMaker(*self.setting)
        self.real_maker = VppRealMaker(self.time_interval, self.id_list)

    def create_data_and_merge(self):
        df = self.prediction_maker.create_interval_prediction(
            "regularly", self.time_interval)
        real = self.real_maker.query_real_data()

        self.merged = pd.merge(
            df, real, how="left", on=["FCST_TM", "location_num"])
        self.merged = self.merged.drop(
            columns=["lat_x", "lon_x", "lat_y", "lon_y"])
        self.merged = self.merged.dropna()


class JenonEval(GeneralEval):
    def __init__(self, time_interval):
        super(JenonEval, self).__init__(time_interval)
        self.loc_jeju = CONSTANT.jeju_coodrinate
        self.loc_nonsan = CONSTANT.nonsan_coordinate

        self.setting = ["unis", [self.loc_jeju, self.loc_nonsan],
                        "nonje_1016model.h5", "rdaps.h5"]

    def make_connection(self):
        self.prediction_maker = GeneralPredictionMaker(*self.setting)
        self.real_maker = JenonRealMaker(self.time_interval)

    def create_data_and_merge(self):
        df = self.prediction_maker.create_interval_prediction(
            "regularly", self.time_interval)
        real = self.real_maker.query_real_data()

        self.merged = pd.merge(
            df, real, how="left", on=["FCST_TM", "location_num"])
        self.merged = self.merged.dropna()
