import datetime
import re

a = 2019101003
converted = datetime.datetime.strptime(str(a), "%Y%m%d%H")
print(converted)


class InputConverter:
    def __init__(self):
        pass

    @staticmethod
    def time_interval_conversion(time_interval):
        start_time = datetime.datetime.strptime(str(time_interval[0]), "%Y%m%d%H")
        end_time = datetime.datetime.strptime(str(time_interval[1]), "%Y%m%d%H")
        return [start_time, end_time]

    @staticmethod
    def current_time_conversion(current_time):
        return datetime.datetime.strptime(str(current_time), "%Y%m%d%H")

