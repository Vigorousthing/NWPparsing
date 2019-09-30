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
        self.output_container = files_container.output_container

    # def extract_value(self, nearest_type=1):
    #     def base_dataframe_with_column(variables, info_file_name):
    #         col = ["CRTN_TM", "horizon", "FCST_TM", "Coordinates"]
    #         if variables == "all":
    #             variables = pd.read_excel(info_file_name).set_index("index")["var_abbrev"].to_list()
    #         for var in variables:
    #             col.append(var)
    #         return pd.DataFrame(columns=col), col
    #
    #     def base_setting(grid_analyzer):
    #         nwp_var_index_dic = file.nwp_var_info.set_index("var_abbrev")["index"]
    #         if grid_analyzer.set_lat_lon_call % 100 == 0:
    #             grid_analyzer.set_lat_lon_grid(pygrib_file[1].latlons()[0], pygrib_file[1].latlons()[1])
    #         return nwp_var_index_dic
    #
    #     try:
    #         file = self.files_container.get()
    #         pygrib_file = pygrib.open(os.path.join(CONSTANT.local_path, file.name))
    #
    #         nwp_var_index_dic = base_setting(self.grid_analyzer)
    #         df, column = base_dataframe_with_column(file.variables, file.info_file_name)
    #
    #         crtn_tm = file.crtn_tm + datetime.timedelta(hours=9)
    #         fcst_tm = file.fcst_tm + datetime.timedelta(hours=9)
    #
    #         for point in file.location_points:
    #             row = [crtn_tm, file.horizon, fcst_tm, point]
    #             for i, var_name in enumerate(file.variables):
    #                 # if i < 4:
    #                 #     # skip crtn_tm, horizon, fcst_tm, point column
    #                 #     continue
    #                 var_index_inside_pygrib_file = nwp_var_index_dic[var_name].item()
    #                 if nearest_type == 1:
    #                     nearest_point_index = self.grid_analyzer.nearest_point_index(point[0], point[1])
    #                     value = pygrib_file[var_index_inside_pygrib_file].values[nearest_point_index[0]][nearest_point_index[1]]
    #                 else:
    #                     var_grid_values = pygrib_file[var_index_inside_pygrib_file].values
    #                     nearest_point_dis_index_dic, _ = self.grid_analyzer.nearest_n_grid_point(point[0], point[1], nearest_type)
    #                     value = self.grid_analyzer.nearest_n_point_weighted_value(var_grid_values, nearest_point_dis_index_dic)
    #                 row.append(value)
    #             row = pd.Series(row, index=column)
    #             df = df.append(row, ignore_index=True)
    #         pygrib_file.close()
    #
    #     except BaseException as e:
    #         print("error occurred: ", e)
    #
    #     # print(file.name)
    #     return df

    # def run(self):
    #     self.df = self.extract_value()
    #     while not self.files_container.empty():
    #         df = self.extract_value()
    #         self.df = self.df.append(df)
    #     self.output_container.put(self.df)

    def extract_value_v2(self, nearest_type=1):
        def base_setting(grid_analyzer):
            nwp_var_index_dic = file.nwp_var_info.set_index("var_abbrev")["index"]
            if grid_analyzer.set_lat_lon_call % 100 == 0:
                grid_analyzer.set_lat_lon_grid(pygrib_file[1].latlons()[0], pygrib_file[1].latlons()[1])
            return nwp_var_index_dic

        try:
            file = self.files_container.get()
            pygrib_file = pygrib.open(os.path.join(CONSTANT.local_path, file.name))

            nwp_var_index_dic = base_setting(self.grid_analyzer)
            crtn_tm = file.crtn_tm + datetime.timedelta(hours=9)
            fcst_tm = file.fcst_tm + datetime.timedelta(hours=9)
            row_num = len(file.location_points)

            df = pd.DataFrame()
            crtn_column = [crtn_tm for i in range(row_num)]
            df["CRTN_TM"] = crtn_column
            df["horizon"] = file.horizon
            df["FCST_TM"] = fcst_tm
            df["Coordinates"] = [point for point in file.location_points]

            if file.variables == "all":
                file.variables = pd.read_excel(file.info_file_name).set_index("index")["var_abbrev"].to_list()

            for i, var_name in enumerate(file.variables):
                var_index_inside_pygrib_file = nwp_var_index_dic[var_name].item()
                value_array = pygrib_file[var_index_inside_pygrib_file].values
                value_list = []
                for point in file.location_points:
                    if nearest_type != 1:
                        nearest_point_dis_index_dic, _ = self.grid_analyzer.nearest_n_grid_point(point[0], point[1], nearest_type)
                        value = self.grid_analyzer.nearest_n_point_weighted_value(value_array, nearest_point_dis_index_dic)
                        value_list.append(value)
                    else:
                        nearest_point_index = self.grid_analyzer.nearest_point_index(point[0], point[1])
                        value = value_array[nearest_point_index[0]][nearest_point_index[1]]
                        value_list.append(value)
                df[var_name] = value_list
            pygrib_file.close()

        except BaseException as e:
            print(e)

        # print(file.name)
        return df

    def run(self):
        self.df = self.extract_value_v2()
        while not self.files_container.empty():
            df = self.extract_value_v2()
            self.df = self.df.append(df)
        self.output_container.put(self.df)
