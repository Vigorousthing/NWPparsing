# import datetime
#
# a = datetime.datetime.now().replace(microsecond=0)
# b = datetime.datetime.now().replace(microsecond=0)
#
# print(int((b-a).total_seconds()))

from controllers.prediction_maker import GeneralPredictionMaker
from data_accessors.MongoDbConnector import get_site_info_df
from util.input_converter import InputConverter
from controllers.real_data_maker import VppRealMaker
import pandas as pd
import numpy as np
import math
import CONSTANT
# prediction_maker = TimeDesignatedPredictionMaker()

checkpoint = False


if checkpoint is not True:
    # set site list
    site_info = get_site_info_df()
    id_list = list(site_info[site_info.capacity == 99]["COMPX_ID"])

    # make prediction & real data
    setting = ["unis", InputConverter().vpp_compx_id_to_coordinates(
        id_list, get_site_info_df()), "nonje_1016model.h5", "rdaps.h5"]
    time_interval = [2019100106, 2019100406]
    prediction_maker = GeneralPredictionMaker(*setting)
    real_maker = VppRealMaker(time_interval, id_list)

    df = prediction_maker.create_interval_prediction("regularly", time_interval)
    real = real_maker.query_real_data()

    # join with key
    merged = pd.merge(df, real, how="left", on=["FCST_TM", "location_num"])
    merged = merged.drop(columns=["lat_x", "lon_x", "lat_y", "lon_y"])

    # filter mergerd df
    # merged = merged[merged.production > 0]
    # merged = merged[merged.horizon == 6]

    # make criteria column
    merged["rmse"] = (merged["production"] - merged["prediction"])**2
    merged["mape"] = abs(merged["production"] - merged["prediction"])
    merged["mbe"] = merged["production"] - merged["prediction"]

    merged.to_excel(CONSTANT.data_file_path + "0106test.xlsx")
else:
    merged = pd.read_excel(CONSTANT.data_file_path + "0106test.xlsx")

# group by horizon
merged = merged.groupby(merged["horizon"])
merged = merged.agg(["count", "mean", "sum"])

merged["rRMSE"] = (merged["rmse"]["sum"].apply(np.sqrt))/(merged[
                                                            "production"][
                                                            "mean"] * merged[
                                                            "production"][
                                                            "count"].apply(
                                                            np.sqrt))
merged["rMBE"] = merged["mbe"]["sum"] / (merged["production"]["mean"] *
                                         merged["production"]["count"])


merged.to_excel(CONSTANT.data_file_path + "merged0106testt.xlsx")
# merged = merged.mean()
# print(merged)

# aggregate from criteria column
# sum_error_square = merged["rmse"].sum()
# rownum = merged.shape[0]
# mean_production = merged["production"].mean()

# rRMSE = (math.sqrt(sum_error_square)/(mean_production*math.sqrt(rownum)))*100
# nMAPE = merged["mape"].mean()/99
# rMBE = (merged["mbe"].sum()/(rownum*mean_production))*100

# print output
# print(rRMSE, nMAPE, rMBE)
