import ftplib
import pygrib
import datetime
from math import *
from haversine import *
import matplotlib.pyplot as plt
import string
import random
from Load_data import *
from data_manipulation import *
import pandas as pd
import time
# temp_file = pygrib.open("l015_v070_erlo_unis_h035.2019030806.gb2")

start_time = time.time()

file_name_list = []
mypath = "/home/jhpark/NWP/"

from os import walk

for a, b, c in walk(mypath):
    file_name_list = c

print(file_name_list)


temp_file = pygrib.open("l015_v070_erlo_unis_h002.2019042318.gb2")
temp_file.close()
# df = pd.DataFrame(temp_file[1].values)
# df.to_pickle("/home/jhpark/experiment_files/" +"nswsw"+ ".pkl")
# df.to_excel("/home/jhpark/experiment_files/" + "nswsw" + ".xlsx")
# df.to_csv("/home/jhpark/experiment_files/" + "nswsw" + ".csv")

# import multiprocessing
# print(multiprocessing.cpu_count())

# a = temp_file[13].values
# a = a.astype(float)
# print(type(a[0][-1]))
# print(len(a[0]))
# a = a.tolist()
# print(a)
#
from pymongo import MongoClient
client = MongoClient("mongodb://10.0.1.40:27017/")
db = client.test_database
collection = db["test_nwp_variable_selection"]

# b = a.tolist()
# collection.insert_one({"fcst_tm": "201906050000", "crtn_tm": "201906051200", "lead_hr": 12, "SWS": b})

# print(collection)
# col1.save({"NDSWS": 1})
# col1.save({"NDSWS": a})


def insert_to(collection, filename):
    path = "/home/jhpark/NWP/"
    file = pygrib.open(path+filename)

    sth = file[1].values
    sth = sth.tolist()

    collection.insert_one({"SWS": sth})
    file.close()

for filename in file_name_list:
    insert_to(collection, filename)
# print(len(file_name_list))

# insert_to(collection, a)

# b = collection.find_one({"fcst_tm": "201906050000", "lead_hr": 12})
# print(b["SWS"])

end_time = time.time()

print("passed: ", end_time - start_time)