import multiprocessing
import datetime
import pandas as pd
import pygrib
import os
import CONSTANT


class IndividualDataCollector(multiprocessing.Process):
    def __init__(self, grid_analyzer, files_container):
        super(IndividualDataCollector, self).__init__()
        self.df = None
        self.grid_analyzer = grid_analyzer
        self.files_container = files_container.container
        self.failed_container = files_container.lead_hr_failed
        self.output_container = files_container.output_container

    def extract_value(self, nearest_type=1):
        df = None

        def base_setting(grid_analyzer):
            nwp_var_index_dic = file.nwp_var_info.set_index(
                "var_abbrev")["index"]
            if grid_analyzer.set_lat_lon_call % 100 == 0:
                lat_lon_grid = pygrib_file[1].latlons()
                grid_analyzer.set_lat_lon_grid(lat_lon_grid[0],
                                               lat_lon_grid[1])
            return nwp_var_index_dic
        try:
            while True:
                if not self.files_container.empty():
                    file = self.files_container.get()
                    break
                elif self.files_container.empty():
                    return

            pygrib_file = pygrib.open(os.path.join(CONSTANT.files_path,
                                                   file.name))
            nwp_var_index_dic = base_setting(self.grid_analyzer)
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
                var_index_inside_pygrib_file = nwp_var_index_dic[var_name].\
                    item()
                value_array = pygrib_file[var_index_inside_pygrib_file].values
                value_list = []
                for point in file.location_points:
                    if nearest_type != 1:
                        nearest_point_dis_index_dic, _ = \
                            self.grid_analyzer.nearest_n_grid_point(
                                point[0], point[1], nearest_type)
                        value = self.grid_analyzer.\
                            nearest_n_point_weighted_value(
                                value_array, nearest_point_dis_index_dic)
                        value_list.append(value)
                    else:
                        nearest_point_index = self.grid_analyzer.\
                            nearest_point_index(point[0], point[1])
                        value = value_array[nearest_point_index[0]][
                            nearest_point_index[1]]
                        value_list.append(value)
                df[var_name] = value_list
            pygrib_file.close()

        except BaseException as e:
            print(e)
            lead_hr = abs(int((file.fcst_tm - datetime.datetime.now() -
                               datetime.timedelta(hours=9)).
                              total_seconds()/3600))
            self.failed_container.append(lead_hr)
            return

        return df

    def extract_value2(self, nearest_type=1):
        df = None

        def base_setting(grid_analyzer):
            nwp_var_index_dic = file.nwp_var_info.set_index(
                "var_abbrev")["index"]
            if grid_analyzer.set_lat_lon_call % 100 == 0:
                lat_lon_grid = pygrib_file[1].latlons()
                grid_analyzer.set_lat_lon_grid(lat_lon_grid[0],
                                               lat_lon_grid[1])
            return nwp_var_index_dic
        try:
            while True:
                if not self.files_container.empty():
                    file = self.files_container.get()
                    break
                elif self.files_container.empty():
                    return

            pygrib_file = pygrib.open(os.path.join(CONSTANT.files_path,
                                                   file.name))
            nwp_var_index_dic = base_setting(self.grid_analyzer)
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

            value_dic = {}
            for i, var_name in enumerate(file.variables):
                var_index_inside_pygrib_file = nwp_var_index_dic[var_name]. \
                    item()
                value_array = pygrib_file[var_index_inside_pygrib_file].values
                value_dic[var_name] = value_array

            nearest_index_dic = {}
            for i, point in enumerate(file.location_points):
                if nearest_type != 1:
                    nearest_point_dis_index_dic, _ = \
                        self.grid_analyzer.nearest_n_grid_point(
                            point[0], point[1], nearest_type)
                    nearest_index_dic[i] = nearest_point_dis_index_dic
                    # value = grid_analyzer. \
                    #     nearest_n_point_weighted_value(
                    #     value_array, nearest_point_dis_index_dic)
                else:
                    nearest_point_index = self.grid_analyzer. \
                        nearest_point_index(point[0], point[1])
                    nearest_index_dic[i] = nearest_point_index
                    # value = value_array[nearest_point_index[0]][
                    #     nearest_point_index[1]]

            for i, var_name in enumerate(file.variables):
                # var_index_inside_pygrib_file = nwp_var_index_dic[var_name]. \
                #     item()
                # value_array = pygrib_file[var_index_inside_pygrib_file].values
                value_array = value_dic[var_name]
                value_list = []
                for i, point in enumerate(file.location_points):
                    if nearest_type != 1:
                        # nearest_point_dis_index_dic, _ = \
                        #     grid_analyzer.nearest_n_grid_point(
                        #         point[0], point[1], nearest_type)
                        value = self.grid_analyzer.nearest_n_point_weighted_value(
                            value_array, nearest_index_dic[i])
                        # value = grid_analyzer. \
                        #     nearest_n_point_weighted_value(
                        #     value_array, nearest_point_dis_index_dic)
                        value_list.append(value)
                    else:
                        # nearest_point_index = grid_analyzer. \
                        #     nearest_point_index(point[0], point[1])
                        # value = value_array[nearest_point_index[0]][
                        #     nearest_point_index[1]]
                        value = value_array[nearest_index_dic[i][0],
                                            nearest_index_dic[i][1]]
                        value_list.append(value)
                df[var_name] = value_list
            pygrib_file.close()

        except BaseException as e:
            print(e)
            lead_hr = abs(int((file.fcst_tm - datetime.datetime.now() -
                               datetime.timedelta(hours=9)).
                              total_seconds()/3600))
            self.failed_container.append(lead_hr)
            return

        return df


    def run(self):
        if self.files_container.empty():
            return
        else:
            result_list = []
            while not self.files_container.empty():
                result = self.extract_value()
                if result is not None:
                    result_list.append(result)

        if len(result_list) == 0:
            return
        else:
            df = result_list.pop()
            for result in result_list:
                df = df.append(result, sort=False)
            self.output_container.put(df)
