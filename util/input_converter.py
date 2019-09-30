import datetime
import re

time_interval = ["2019-09-10 00", "2019-10-10 03"]

start_time = datetime.datetime.strptime(time_interval[0], "%Y-%m-%d %H")

a = 2019101003
converted = datetime.datetime.strptime(str(a), "%Y%m%d%H")
print(converted)





class InputConverter:
    def __init__(self):
        pass

    def time_interval_conversion(self, time_interval):
        start_time = datetime.datetime.strptime(str(time_interval[0]), "%Y%m%d%H")
        end_time = datetime.datetime.strptime(str(time_interval[1]), "%Y%m%d%H")
        return

    def current_time_conversion(self, current_time):
        pass