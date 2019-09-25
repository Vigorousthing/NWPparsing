import pymongo
import CONSTANT
import pandas as pd
from new_model_creation import *
from pandas.io.json import json_normalize

pipeline_for_real = [{"$project": { "COMPX_ID": 1, "hourly": 1, "date": {"$dateFromString": {"dateString": '$CRTN_TM'}}}},\
                    {"$sort": {"date": 1, "COMPX_ID": 1}}, \
                    {"$group": {"_id": {"COMPX_ID": '$COMPX_ID', "lastDate": {"$dateToString": {"format":'%Y%m%d', "date": '$date'}}}, "lastHourly": {"$last": '$hourly'}}}, \
                    {"$unwind": {"path": '$lastHourly', "includeArrayIndex": 'arrayIndex'}}, \
                    {"$project":{"_id": {"COMPX_ID" : 1, "lastDate": 1, "hour": '$arrayIndex'}, "lastHourly": 1}}, \
                    {"$project":{"site": '$_id.COMPX_ID', "production": '$lastHourly', "date": {"$dateFromString": { "dateString": '$_id.lastDate'}}}}, \
                    {"$project":{"production": 1, "site": 1, "temp": {"$dateToParts" : {"date":'$date'}}}}, \
                    {"$project":{"production": 1, "site": 1, "timestamp": {"$dateFromParts": {'year' : '$temp.year', 'month' : '$temp.month', 'day': '$temp.day', 'hour' : '$_id.hour'}}}}, \
                    {"$project":{"production": 1, "site": 1, "timestamp": {"$dateToString":{"format":'%Y%m%d%H', "date": '$timestamp'}}}}]


class MongodbConnector:
    def __init__(self, db_name, collection_name):
        self.conn = pymongo.MongoClient(CONSTANT.mongodb_ip, CONSTANT.mongodb_port)
        self.db = self.conn.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def aggregate(self, query, disk_use=True):
        return self.collection.aggregate(query, allowDiskUse=disk_use)

    def find_latest(self):
        return self.collection.find().sort([("_id", -1)]).limit(1)


def get_sitelist(latest_document):
    result = pd.DataFrame(list(latest_document)[0]["sites_list"])
    result = result.drop(columns=["address", "contract", "facility", "name", "network", "installdoc", "state",
                                  "subscription",
                                  "updated"])
    result["Coordinates"] = result.apply(lambda row: (float(row.lat), float(row.lng)), axis=1)
    return result


if __name__ == "__main__":
    # mongodb_connector = MongodbConnector("sites", "production")
    # result = mongodb_connector.aggregate(pipeline_for_real)
    # result = pd.DataFrame(list(result))

    site_list_connector = MongodbConnector("sites", "sitesList")
    result = get_sitelist(site_list_connector.find_latest())

    coordinate_list = result["Coordinates"].get_values().tolist()
