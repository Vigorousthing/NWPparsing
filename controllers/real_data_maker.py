from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.DbConnector import *
from data_accessors.MongoDbConnector import *
from util.query_maker import *
from util.input_converter import *
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.QueueJobProgressIndicator import QueueJobProgressIndicator
from util.input_converter import InputConverter
import keras
import time
import numpy as np
import pandas as pd
import datetime


class VppRealMaker:
    def __init__(self, time_interval, plant_id_list):
        self.plant_id_list = plant_id_list
        self.time_interval = time_interval

        self.mongo_connector = MongodbConnector("sites", "production")
        self.site_info_df = self.siteinfo_with_location_num()

    def query_real_data(self):
        result = self.mongo_connector.aggregate(
            vpp_production_query(self.time_interval,
                                 match_plant_subquery(self.plant_id_list)))
        result = result.drop(columns=["_id"])

        result = pd.merge(result, self.site_info_df, how="left",
                          on=["COMPX_ID"])
        result = result.rename(columns={"CRTN_TM": "FCST_TM", "lng": "lon"})
        return result

    def siteinfo_with_location_num(self):
        location_num_table = pd.DataFrame(
            list(zip(self.plant_id_list, [i for i in range(len(
                self.plant_id_list))])),
            columns=["COMPX_ID", "location_num"])
        result = pd.merge(location_num_table, get_site_info_df(), how="left",
                          on=["COMPX_ID"])
        print(result)
        return result


class JenonRealMaker:
    def __init__(self, time_interval):
        self.time_interval = time_interval
        self.input_converter = InputConverter()

        self.jeju_connector = JejuDbConnector()
        self.nonsan_connector = NonsanDbConnector()

    def query_real_data(self):
        time_interval = self.input_converter.date_buffer_for_real_data(
            self.time_interval)
        time_interval = self.input_converter.int_date_to_string_date(
            self.time_interval)

        jeju_real = pd.DataFrame(self.jeju_connector.query(jenon_sql.format(
            time_interval[0], time_interval[1])))
        nonsan_real = pd.DataFrame(self.nonsan_connector.query(
            jenon_sql.format(time_interval[0], time_interval[1])))

        jeju_real = jeju_real.rename(columns={"sum(tbl_inverter_min.KWD)":
                                                  "production",
                                              "tbl_inverter_min.recvdate - "
                                              "INTERVAL 10 MINUTE": "FCST_TM"})
        jeju_real["location_num"] = 0
        nonsan_real = nonsan_real.rename(columns={"sum(tbl_inverter_min.KWD)":
                                                  "production",
                                              "tbl_inverter_min.recvdate - "
                                              "INTERVAL 10 MINUTE": "FCST_TM"})
        nonsan_real["location_num"] = 1

        return jeju_real.append(nonsan_real)


if __name__ == '__main__':
    a = VppRealMaker([2019080100, 2019080323],
                     ["P31S2105", "P31S51157", "P61S2102"])
    b = JenonRealMaker([2019080100, 2019080323])
    df = b.load_real_data()
    print(df)
