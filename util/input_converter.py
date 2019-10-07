import datetime
import pandas as pd
import CONSTANT


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

    @staticmethod
    def vpp_compx_id_to_coordinates(id_list):
        info_df = pd.read_excel(CONSTANT.setting_file_path +
                                "vpp_plant_location_info.xlsx")
        coordinate_list = []
        for i in id_list:
            idx = info_df[info_df["site_id"] == i].index.tolist()[0]
            row_list = info_df.iloc[idx].tolist()
            coordinate = (row_list[2], row_list[3])
            coordinate_list.append(coordinate)
        return coordinate_list
