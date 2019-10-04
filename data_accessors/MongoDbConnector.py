import re
import pymongo
import CONSTANT
import datetime
import pandas as pd
from pandas.io.json import json_normalize
from util.input_converter import InputConverter


class MongodbConnector:
    def __init__(self, db_name, collection_name):
        self.conn = pymongo.MongoClient(CONSTANT.mongodb_ip, CONSTANT.mongodb_port)
        self.db = self.conn.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def aggregate(self, query, disk_use=True):
        return pd.DataFrame(list(self.collection.aggregate(
            query, allowDiskUse=disk_use)))

    def find_latest(self):
        return self.collection.find().sort([("_id", -1)]).limit(1)


def get_sitelist(latest_document):
    result = pd.DataFrame(list(latest_document)[0]["sites_list"])
    result = result.drop(columns=["address", "contract", "facility", "name",
                                  "network", "installdoc", "state",
                                  "subscription", "updated"])
    result["Coordinates"] = result.apply(lambda row: (
        float(row.lat), float(row.lng)), axis=1)
    return result


def vpp_production_query(time_interval, add_query=None):
    converter = InputConverter()

    start_time, end_time = converter.time_interval_conversion(time_interval)
    start_time = start_time - datetime.timedelta(hours=120)
    end_time = end_time + datetime.timedelta(hours=120)

    start_time = converter.string_conversion(start_time).ljust(12, "0")
    end_time = converter.string_conversion(end_time).ljust(12, "0")

    first_query = {"$match": {"CRTN_TM": {"$gt": "{}".format(start_time),
                            "$lt": "{}".format(end_time)}}}
    pipeline_for_real = [
        {"$project": {"COMPX_ID": 1, "hourly": 1, "date": {"$dateFromString": {"dateString": "$CRTN_TM"}}}},
        {"$project": {"COMPX_ID": 1, "hourly": 1, "date": 1, "hour": {"$hour": "$date"}}},
        {"$sort": {"date": 1, "COMPX_ID": 1}}, {"$match": {"hour": 22}},
        {"$unwind": {"path": "$hourly", "includeArrayIndex": "arrayIndex"}},
        {"$project": {"hourly": 1, "COMPX_ID": 1, "date": 1, "hour": 1, "arrayIndex": 1,
                      "parts": {"$dateToParts": {"date": "$date"}}}},
        {"$project": {"hourly": 1, "COMPX_ID": 1, "date": 1, "hour": 1, "arrayIndex": 1, "parts": 1,
                      "agg": {"$dateFromParts": {"year": "$parts.year", "month": "$parts.month", "day": "$parts.day",
                                                 "hour": "$arrayIndex"}}}},
        {"$project": {"CRTN_TM": "$agg", "production": "$hourly", "COMPX_ID": 1}}
    ]
    if add_query is not None:
        pipeline_for_real.insert(0, add_query)
    pipeline_for_real.insert(0, first_query)
    return pipeline_for_real
