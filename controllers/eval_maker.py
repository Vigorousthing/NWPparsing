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
        self.merged["rmse"] = (
            self.merged["production"] - self.merged["prediction"]) ** 2
        self.merged["mape"] = abs(
            self.merged["production"] - self.merged["prediction"])
        self.merged["mbe"] = self.merged["production"]\
                             - self.merged["prediction"]
        self.merged = self.merged.groupby(self.merged["horizon"])
        self.merged = self.merged.agg(["count", "mean", "sum"])

    def cal_final_criteria(self):
        self.merged["rRMSE"] = (self.merged["rmse"]["sum"].apply(np.sqrt)) / \
           (self.merged["production"]["mean"] *
            self.merged["production"]["count"].apply(np.sqrt))
        self.merged["rMBE"] = self.merged["mbe"]["sum"] / \
            (self.merged["production"]["mean"] *
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
        self.loc_jeju = CONSTANT.jenon_coordinates[0]
        self.loc_nonsan = CONSTANT.jenon_coordinates[1]

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


class SimpleEval:
    def __init__(self):
        self.merged = None
        self.eval_criteria = ["rmse", "nrmse", "mae", "nmae", "mbe", "nmbe",
                              "mape", "nmape"]

    def set_through_file(self, filename):
        self.merged = pd.read_excel(CONSTANT.data_file_path + filename)

    def set_through_files(self, nwp_filename, real_filename):
        nwp_df = pd.read_excel(CONSTANT.data_file_path + nwp_filename)
        real_df = pd.read_excel(CONSTANT.data_file_path + real_filename)
        self.merged = pd.merge(
            nwp_df, real_df, how="left", on=["FCST_TM", "location_num"])
        self.merged = self.merged.dropna()

    def eval(self):
        self.merged["dif"] = self.merged["production"] - \
                             self.merged["prediction"]
        self.merged["dif_abs"] = abs(self.merged["dif"])
        self.merged["dif_sqr"] = self.merged["dif"] ** 2

        self.merged["real_variance"] = np.square(
            self.merged["production"] - np.mean(self.merged["production"]))

        self.merged["dif_div_capa_sqr"] = \
            ((self.merged["production"] - self.merged["prediction"]) /
             self.merged["capacity"]) ** 2
        self.merged["dif_div_real_abs"] = \
            abs((self.merged["production"] - self.merged["prediction"]) /
                self.merged["production"])
        self.merged["dif_div_capa_abs"] = \
            abs((self.merged["production"] - self.merged["prediction"]) /
                self.merged["capacity"])

        self.merged = self.merged.groupby("lead_hr").mean()

        self.merged["rmse"] = np.sqrt(self.merged["dif_sqr"])
        self.merged["nrmse"] = np.sqrt(self.merged["dif_div_capa_sqr"]) * 100
        self.merged["mae"] = self.merged["dif_abs"]
        self.merged["nmae"] = self.merged["dif_abs"] / self.merged[
            "production"]
        self.merged["mbe"] = self.merged["dif"]
        self.merged["nmbe"] = self.merged["dif"] / self.merged["production"]
        self.merged["mape"] = self.merged["dif_div_real_abs"]
        self.merged["nmape"] = self.merged["dif_div_capa_abs"]

        self.merged["r-squared"] = 1 - (self.merged["dif_sqr"] / self.merged[
            "real_variance"])

        # self.merged.to_excel(CONSTANT.data_file_path +
        #                      "rsqrdtest20200203.xlsx")
        print(self.merged)

    def _eval(self, merged_df):
        # merged_df = merged_df[merged_df.real > (0.1 * merged_df.capacity)]
        merged_df["prediction"] = (merged_df["prediction"] / 612) * \
                                  merged_df["capacity"]

        merged_df["dif"] = merged_df["real"] - \
                             merged_df["prediction"]
        merged_df["dif_abs"] = abs(merged_df["dif"])
        merged_df["dif_sqr"] = merged_df["dif"] ** 2

        merged_df["real_variance"] = np.square(
            merged_df["real"] - np.mean(merged_df["real"]))

        merged_df["dif_div_capa_sqr"] = \
            ((merged_df["real"] - merged_df["prediction"]) /
             merged_df["capacity"]) ** 2
        merged_df["dif_div_real_abs"] = \
            abs((merged_df["real"] - merged_df["prediction"]) /
                merged_df["real"])
        merged_df["dif_div_capa_abs"] = \
            abs((merged_df["real"] - merged_df["prediction"]) /
                merged_df["capacity"])

        merged_df = merged_df.groupby("horizon").mean()

        merged_df["rmse"] = np.sqrt(merged_df["dif_sqr"])
        merged_df["nrmse"] = np.sqrt(merged_df["dif_div_capa_sqr"]) * 100
        merged_df["mae"] = merged_df["dif_abs"]
        merged_df["nmae"] = merged_df["dif_abs"] / merged_df["real"]
        merged_df["mbe"] = merged_df["dif"]
        merged_df["nmbe"] = merged_df["dif"] / merged_df["real"]
        merged_df["mape"] = merged_df["dif_div_real_abs"]
        merged_df["nmape"] = merged_df["dif_div_capa_abs"]

        merged_df["r-squared"] = 1 - (merged_df["dif_sqr"] / merged_df[
            "real_variance"])

        print(merged_df)
        print(merged_df.describe())

        return merged_df


if __name__ == '__main__':
    evaler = SimpleEval()
    evaler.set_through_file("evalexp20200131.xlsx")

    evaler.eval()
