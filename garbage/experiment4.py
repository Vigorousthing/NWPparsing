import numpy as np
import pandas as pd
import re
import datetime

col = ["fcst_tm", "crtn_tm", "value"]

a = [1, 2, 3]
b = [4, 5, 6]

df = pd.DataFrame(columns=col)
a = pd.Series(a, index=col)
b = pd.Series(b, index=col)
df = df.append(a, ignore_index=True)
df = df.append(b, ignore_index=True)


print df


string = "l015_v070_erlo_unis_h036.2019041618.gb2"

print re.sub('[^A-Za-z0-9]+', '', str(string))
print re.sub('[^z0-9]+', '', str(string))

print string.split("h")[1].split(".")

start_time = "2019041618"
start_time = datetime.datetime.strptime(start_time, "%Y%m%d%H")
print start_time
print int("019")
# print 17%6
# import haversine
# a = (10,20)
# b = (10,21)
# print haversine.haversine(a, b)
# print haversine.haversine((45.7597, 4.8422), (48.8567, 2.3508))