import datetime


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
            var_list = list(pd.read_excel(path)["var_abbrev"])
            print(var_list)
        else:
            variable = variable
        return variable


if __name__ == '__main__':
    test = InputConverter()
    from nwp_object.NwpFile import *
    test.convert_to_variable_list("all", RdapsFile)
