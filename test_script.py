import multiprocessing
import datetime
import pandas as pd
import pygrib
import os
import CONSTANT
from util.NwpGridAnalyzer import NwpGridAnalyzer
from nwp_object import NwpFile
from util.input_converter import InputConverter


def extract_value(nearest_type=1):
    df = None

    def base_setting(grid_analyzer):
        info_file_name = CONSTANT.ldaps_variable_index_file_name
        nwp_var_info = pd.read_excel(
            os.path.join(CONSTANT.setting_file_path, info_file_name))
        nwp_var_index_dic = nwp_var_info.set_index(
            "var_abbrev")["index"]
        if grid_analyzer.set_lat_lon_call % 100 == 0:
            grid_analyzer.set_lat_lon_grid(
                pygrib_file[1].latlons()[0], pygrib_file[1].latlons()[1])
        return nwp_var_index_dic

    file = NwpFile.LdapsFile("unis", 13,
                             InputConverter.current_time_conversion(
                                 2019121300),
                             CONSTANT.jenon_coordinates, ["TMP"])

    grid_analyzer = NwpGridAnalyzer()

    pygrib_file = pygrib.open(os.path.join(CONSTANT.files_path,
                                           "l015_v070_erlo_unis_h039.2019100112.gb2"))
    nwp_var_index_dic = base_setting(grid_analyzer)
    crtn_tm = file.crtn_tm + datetime.timedelta(hours=9)
    fcst_tm = file.fcst_tm + datetime.timedelta(hours=9)
    row_num = len(file.location_points)

    df = pd.DataFrame()
    crtn_column = [crtn_tm for i in range(row_num)]
    df["CRTN_TM"] = crtn_column
    df["horizon"] = file.horizon
    df["FCST_TM"] = fcst_tm
    df["lat"] = [point[0] for point in file.location_points]
    df["lon"] = [point[1] for point in file.location_points]
    df["location_num"] = [i for i in range(len(file.location_points))]

    if file.variables == "all":
        file.variables = pd.read_excel(file.info_file_name).set_index(
            "index")["var_abbrev"].to_list()

    for i, var_name in enumerate(file.variables):
        var_index_inside_pygrib_file = nwp_var_index_dic[var_name]. \
            item()
        value_array = pygrib_file[var_index_inside_pygrib_file].values
        value_list = []
        for point in file.location_points:
            if nearest_type != 1:
                nearest_point_dis_index_dic, _ = \
                    grid_analyzer.nearest_n_grid_point(
                        point[0], point[1], nearest_type)
                value = grid_analyzer. \
                    nearest_n_point_weighted_value(
                    value_array, nearest_point_dis_index_dic)
                value_list.append(value)
            else:
                nearest_point_index = grid_analyzer. \
                    nearest_point_index(point[0], point[1])
                value = value_array[nearest_point_index[0]][
                    nearest_point_index[1]]
                value_list.append(value)
        df[var_name] = value_list
    pygrib_file.close()

    return df


print(extract_value())