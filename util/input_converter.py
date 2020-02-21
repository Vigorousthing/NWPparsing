import CONSTANT
import datetime
import pandas as pd
import os


class InputConverter:
    def __init__(self):
        pass

    @staticmethod
    def time_interval_conversion(time_interval_int_list):
        start_time = datetime.datetime.strptime(
            str(time_interval_int_list[0]), "%Y%m%d%H")
        end_time = datetime.datetime.strptime(
            str(time_interval_int_list[1]), "%Y%m%d%H")
        return [start_time, end_time]

    @staticmethod
    def current_time_conversion(current_time_int):
        if type(current_time_int) == datetime.datetime:
            return current_time_int
        return datetime.datetime.strptime(str(current_time_int), "%Y%m%d%H")

    @staticmethod
    def current_time_conversion_12char(current_time_int):
        if type(current_time_int) == datetime.datetime:
            return current_time_int
        return datetime.datetime.strptime(str(current_time_int), "%Y%m%d%H%M")

    @staticmethod
    def string_conversion(time):
        return datetime.datetime.strftime(time, "%Y%m%d%H")

    @staticmethod
    def vpp_compx_id_to_coordinates(id_list, site_info_df):
        if id_list == "all":
            return list(site_info_df["Coordinates"])
        else:
            site_info_df = site_info_df[site_info_df["COMPX_ID"].isin(
                id_list)]
            return list(site_info_df["Coordinates"])

    @staticmethod
    def int_date_to_string_date(time_interval):
        result = []
        for i in time_interval:
            converted = datetime.datetime.strptime(str(i), "%Y%m%d%H")
            result_string = "{}-{}-{}"
            result_string = result_string.format(
                converted.year, converted.month, converted.day)
            result.append(result_string)
        return result

    @staticmethod
    def datetime_to_string_date(time_interval):
        result = []
        for i in time_interval:
            result_string = "{}-{}-{}"
            result_string = result_string.format(
                i.year, i.month, i.day)
            result.append(result_string)
        return result

    @staticmethod
    def date_buffer_for_real_data(time_interval):
        return [time_interval[0] - datetime.timedelta(days=4),
                time_interval[1] + datetime.timedelta(days=4)]

    @staticmethod
    def convert_to_variable_list(variable, file_type):
        if variable == "all":
            path = CONSTANT.setting_file_path + file_type.info_file_name
            variable = list(pd.read_excel(path)["var_abbrev"])
        else:
            variable = variable
        return variable

    @staticmethod
    def save_filename_for_signiture_location(time_interval, coordinates):
        today = datetime.datetime.today()
        today_str = str(today.year) + str(today.month) + str(today.day)
        if len(coordinates) == 2:
            signiture = "nj"
        elif len(coordinates) == 4:
            signiture = "sgv"
        return "{}y{}m{}w_{}_{}".format(str(time_interval[0])[0:4],
                                        str(time_interval[0])[4:6].zfill(2),
                                        (int(str(time_interval[0])[6:8]) //
                                         7) + 1,
                                        signiture,
                                        today_str)

    @staticmethod
    def time_interval_from_m_w(year, month, week_th):
        max_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if year % 400 == 0:
            max_day[1] = 29
        elif year % 100 == 0:
            max_day[1] = 28
        elif year % 4 == 0:
            max_day[1] = 29
        else:
            max_day[1] = 28

        if month == 2 and week_th == 5:
            print("this year, February has only 28 days")
            return
        elif week_th > 5:
            print("No month has more than 5 weeks")
            return

        start_day = int("{}{}{}00".format(year, str(month).zfill(2),
                                      str((week_th - 1) * 7 + 1).zfill(2)))
        if week_th == 5:
            end_day = int("{}{}{}23".format(year, str(month).zfill(2),
                                    str(max_day[month - 1])))
        else:
            end_day = int("{}{}{}23".format(year, str(month).zfill(2),
                                    str((week_th - 1) * 7 + 1 + 6).zfill(2)))

        time_interval = [start_day, end_day]
        return time_interval

    def merge_files_by_horizontally(self):

        pass





if __name__ == '__main__':
    converter = InputConverter()
    a = converter.save_filename_for_signiture_location([2019100800,
                                                        2019101423],
                                                       [(33.2875,
                                                         126.648611),
                                                        (36.149019,
                                                         127.176031)])
    print(a)

    class A:
        _a = 1
        a = 2

    b = A()
    print(b.a)
    print(b._a)

