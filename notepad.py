import datetime
import re

time_interval = ["2019-09-10 00", "2019-10-10 03"]

start_time = datetime.datetime.strptime(time_interval[0], "%Y-%m-%d %H")
start_time.strftime("%Y%m%d%H")

a = datetime.datetime.strftime(start_time, "%Y%m%d%H")
print(a)

print(type(start_time) == datetime.datetime)