import re
import pymongo
import CONSTANT
import datetime
import pandas as pd
from new_model_creation import *
from pandas.io.json import json_normalize


class MongodbConnector:
    def __init__(self, db_name, collection_name):
        self.conn = pymongo.MongoClient(CONSTANT.mongodb_ip, CONSTANT.mongodb_port)
        self.db = self.conn.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def aggregate(self, query, disk_use=True):
        return pd.DataFrame(list(self.collection.aggregate(query, allowDiskUse=disk_use)))

    def find_latest(self):
        return self.collection.find().sort([("_id", -1)]).limit(1)


def get_sitelist(latest_document):
    result = pd.DataFrame(list(latest_document)[0]["sites_list"])
    result = result.drop(columns=["address", "contract", "facility", "name", "network", "installdoc", "state",
                                  "subscription", "updated"])
    result["Coordinates"] = result.apply(lambda row: (float(row.lat), float(row.lng)), axis=1)
    return result


def vpp_production_query(time_interval):
    start_time = datetime.datetime.strptime(time_interval[0], "%Y-%m-%d %H") \
                 - datetime.timedelta(hours=120)
    end_time = datetime.datetime.strptime(time_interval[1], "%Y-%m-%d %H") \
               + datetime.timedelta(hours=120)
    start_time = start_time.strftime("%Y%m%d%H").zfill(12)
    end_time = end_time.strftime("%Y%m%d%H").zfill(12)

    pipeline_for_real = [
        {"$match": {"CRTN_TM": {"$gt": "{}".format(start_time), "$lt": "{}".format(end_time)}}},
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
    return pipeline_for_real


if __name__ == "__main__":
    mongodb_connector = MongodbConnector("sites", "production")
    result = mongodb_connector.aggregate(vpp_production_query([]))
    # result = pd.DataFrame(list(result))
    print(result)

    # site_list_connector = MongodbConnector("sites", "sitesList")
    # result = get_sitelist(site_list_connector.find_latest())
    #
    # coordinate_list = result["Coordinates"].get_values().tolist()
