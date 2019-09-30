import datetime


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
        if type(current_time) == datetime.datetime:
            return current_time
        return datetime.datetime.strptime(str(current_time), "%Y%m%d%H")

    @staticmethod
    def string_conversion(time):
        return datetime.datetime.strftime(time, "%Y%m%d%H")


