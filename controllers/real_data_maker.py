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


class VppDataMaker:
    def __init__(self, time_interval, plant_id_list):
        self.plant_id_list = plant_id_list
        self.time_interval = time_interval

        self.mongo_connector = MongodbConnector("sites", "production")
        self.site_info_df = self.site_info_initialize()

    def create_real_vpp(self):
        mongo_connector = MongodbConnector("sites", "production")
        query = vpp_production_query(self.time_interval,
                                     match_plant_subquery(self.plant_id_list))

        real_df = mongo_connector.aggregate(query)

        real_df = real_df.drop(columns=["_id"])

        merged = pd.merge(real_df, self.site_info_df, how="left",
                          on=["COMPX_ID"])
        merged = merged.rename(columns={"CRTN_TM": "FCST_TM"})
        merged = merged.rename(columns={"lng": "lon"})

        return merged

    def site_info_initialize(self):
        mongo_connector2 = MongodbConnector("sites", "sitesList")
        location_num_table = pd.DataFrame(
            list(zip(self.plant_id_list, [i for i in range(len(
                self.plant_id_list))])),
            columns=["COMPX_ID", "location_num"])
        site_info_df = get_sitelist(mongo_connector2.find_latest())
        site_info_df = site_info_df.rename(columns={"site": "COMPX_ID"})
        site_info_df = pd.merge(site_info_df, location_num_table, how="left",
                                on=["COMPX_ID"])
        return site_info_df


class JenonDataMaker:
    def __init__(self):

        pass
