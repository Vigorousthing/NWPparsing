import datetime
import re
import pygrib
import matplotlib.pyplot as plt
from math import *
from haversine import *
import pandas as pd
import CONSTANT
import os
import multiprocessing
import ftplib
import sys


class NwpFiles:
    full_horizon = None
    prediction_interval = None
    nwp_type = None
    prefix = None
    info_file_name = None
    nwp_var_info = None

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        self.name = "{}_{}_h{}.{}.gb2"
        self.crtn_tm = None
        self.fcst_tm = None
        self.horizon = horizon

        self.probable_crtn_tm = {}

        self.location_points = location_points
        self.variables = variables

        self.set_property(fold, horizon, crtn_tm)
        self.generate_probable_crtn_tm()

    def set_property(self, fold, horizon, crtn_tm):
        self.name = self.name.format(self.prefix, fold, str(horizon).zfill(3), crtn_tm)
        self.crtn_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H")
        self.fcst_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H") + datetime.timedelta(hours=horizon)

    def generate_probable_crtn_tm(self):
        for i in range(6):
            self.probable_crtn_tm[i] = self.crtn_tm + datetime.timedelta(hours=i)


class LdapsFile(NwpFiles):
    full_horizon = 48
    prediction_interval = 1
    nwp_type = "LDAPS"
    prefix = "l015_v070_erlo"
    info_file_name = CONSTANT.ldaps_variable_index_file_name
    nwp_var_info = pd.read_excel(CONSTANT.setting_file_path+info_file_name)

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        super(LdapsFile, self).__init__(fold, horizon, crtn_tm, location_points, variables)


class RdapsFile(NwpFiles):
    full_horizon = 87
    prediction_interval = 3
    nwp_type = "RDAPS"
    prefix = "g120_v070_erea"
    info_file_name = CONSTANT.rdaps_variable_index_file_name
    nwp_var_info = pd.read_excel(CONSTANT.setting_file_path+info_file_name)

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        super(RdapsFile, self).__init__(fold, horizon, crtn_tm, location_points, variables)


class FilesContainer:
    def __init__(self, container_class, time_interval, fold_type, location_points, variables):
        self.type = container_class
        self.fold_type = fold_type
        self.location_points = location_points
        self.variables = variables

        self.current_time = None

        self.start_time, self.end_time = self.time_alignment(time_interval)

        self.container = multiprocessing.Manager().Queue()
        self.output_container = multiprocessing.Manager().Queue()

        self.filename_list = []

    def generate_base_files(self):
        current_time = self.start_time
        while current_time <= self.end_time:
            date_string = re.sub('[^A-Za-z0-9]+', '', str(current_time))[:-4]
            for horizon in range(self.type.full_horizon + 1):
                if horizon % self.type.prediction_interval == 0:
                    file_object = self.type(self.fold_type, horizon, date_string, self.location_points, self.variables)
                    self.container.put(file_object)
                    self.filename_list.append(file_object.name)
            current_time = current_time + datetime.timedelta(hours=6)

    @staticmethod
    def time_alignment(time_interval):
        start_time = datetime.datetime.strptime(time_interval[0], "%Y-%m-%d %H") - datetime.timedelta(hours=9)
        end_time = datetime.datetime.strptime(time_interval[1], "%Y-%m-%d %H") - datetime.timedelta(hours=9)
        if start_time.hour % 6 != 0:
            start_time = start_time + datetime.timedelta(hours=(6 - (start_time.hour % 6)))
        if end_time.hour % 6 != 0:
            end_time = end_time - datetime.timedelta(hours=end_time.hour % 6)
        return start_time, end_time


class FtpAccessor:
    def __init__(self, ip, id, pw):
        self.ip = ip
        self.id = id
        self.pw = pw

        self.ftp = ftplib.FTP()

        # how to check connection
        self.ftp.connect(ip)
        self.ftp.login(id, pw)

    def download_files(self, filename_list, file_type):
        self.ftp.cwd(CONSTANT.ftp_ROOT + file_type)

        for filename in filename_list:
            path = os.path.join(CONSTANT.download_path, filename)
            if os.path.exists(path):
                print(CONSTANT.already_exists_text.format(filename))
                continue
            else:
                try:
                    new_file = open(path, "wb")
                    self.ftp.retrbinary("RETR " + filename, new_file.write)
                    new_file.close()
                except ftplib.error_perm:
                    os.remove(path)
                    # new_file.close()
                    print(CONSTANT.download_exception_text.format(filename))

        self.ftp.close()

    def reconnect(self):
        self.ftp.connect(self.ip)
        self.ftp.login(self.id, self.pw)

    def check_connection(self):
        try:
            self.ftp.voidcmd("NOOP")
        except AttributeError:
            return False
        else:
            return True

    def size_check(self, filename_list, file_type):
        self.ftp.cwd(CONSTANT.ftp_ROOT + file_type)

        file_size = 0
        file_num = 0
        for file_name in filename_list:
            path = os.path.join(CONSTANT.local_path, file_name)
            if not os.path.exists(path):
                try:
                    file_size += self.ftp.size(file_name)
                    file_num += 1
                except ftplib.error_perm:
                    print(file_name + " not exists in ftp server")
        print("total size of files : ", float(file_size) / (1024 * 1024 * 1024), "gb", ", total number of files :",
              file_num)

    def remove_from_local_pc(self, filename_list):
        for filename in filename_list:
            path = os.path.join(CONSTANT.local_path, filename)
            if os.path.exists(path):
                os.remove(path)
            else:
                print("cannot remove " + filename + " because the file does not exists in local pc")

    def close(self):
        self.ftp.close()


class IndividualDataCollector(multiprocessing.Process):
    def __init__(self, grid_analyzer, files_container):
        super(IndividualDataCollector, self).__init__()
        self.df = None
        self.grid_analyzer = grid_analyzer
        self.files_container = files_container.container
        self.output_container = files_container.output_container

    def extract_value(self, nearest_type=1):
        def base_dataframe_with_column(variables, info_file_name):
            col = ["CRTN_TM", "horizon", "FCST_TM", "Coordinates"]
            if variables == "all":
                variables = pd.read_excel(info_file_name).set_index("index")["var_abbrev"].to_list()
            for var in variables:
                col.append(var)
            return pd.DataFrame(columns=col), col

        def base_setting(grid_analyzer):
            nwp_var_index_dic = file.nwp_var_info.set_index("var_abbrev")["index"]
            if grid_analyzer.set_lat_lon_call % 100 == 0:
                grid_analyzer.set_lat_lon_grid(pygrib_file[1].latlons()[0], pygrib_file[1].latlons()[1])
            return nwp_var_index_dic

        try:
            file = self.files_container.get()
            pygrib_file = pygrib.open(os.path.join(CONSTANT.local_path, file.name))

            nwp_var_index_dic = base_setting(self.grid_analyzer)
            df, column = base_dataframe_with_column(file.variables, file.info_file_name)

            crtn_tm = file.crtn_tm + datetime.timedelta(hours=9)
            fcst_tm = file.fcst_tm + datetime.timedelta(hours=9)

            for point in file.location_points:
                row = [crtn_tm, file.horizon, fcst_tm, point]
                for i, var_name in enumerate(file.variables):
                    # if i < 4:
                    #     # skip crtn_tm, horizon, fcst_tm, point column
                    #     continue
                    var_index_inside_pygrib_file = nwp_var_index_dic[var_name].item()
                    if nearest_type == 1:
                        nearest_point_index = self.grid_analyzer.nearest_point_index(point[0], point[1])
                        value = pygrib_file[var_index_inside_pygrib_file].values[nearest_point_index[0]][nearest_point_index[1]]
                    else:
                        var_grid_values = pygrib_file[var_index_inside_pygrib_file].values
                        nearest_point_dis_index_dic, _ = self.grid_analyzer.nearest_n_grid_point(point[0], point[1], nearest_type)
                        value = self.grid_analyzer.nearest_n_point_weighted_value(var_grid_values, nearest_point_dis_index_dic)
                    row.append(value)
                row = pd.Series(row, index=column)
                df = df.append(row, ignore_index=True)
            pygrib_file.close()

        except BaseException as e:
            print(e)

        # print(file.name)
        return df

    def run(self):
        self.df = self.extract_value()
        while not self.files_container.empty():
            df = self.extract_value()
            self.df = self.df.append(df)
        self.output_container.put(self.df)


class DataOrganizer:
    def __init__(self, grid_analyzer, files_container):
        self.total_df = None

        self.grid_analyzer = grid_analyzer
        self.files_container = files_container

        self.individual_collector = {}

    def data_collect(self, num_of_indiv_collector):
        for i in range(num_of_indiv_collector):
            self.individual_collector[i] = IndividualDataCollector(self.grid_analyzer, self.files_container)
            self.individual_collector[i].start()
        for i in range(num_of_indiv_collector):
            self.individual_collector[i].join()

        self.total_df = self.files_container.output_container.get()
        for i in range(1, num_of_indiv_collector):
            self.total_df = self.total_df.append(self.files_container.output_container.get())

        # for i in range(num_of_indiv_collector):
        #     self.individual_collector[i].close()
        # self.total_df = self.individual_collector[0].df
        # for i in range(1, num_of_indiv_collector):
        #     self.total_df = self.total_df.append(self.individual_collector[i].df)
        return self.total_df


class Visualizer:
    def __init__(self):
        pass

    def correlation_matrix(self, df, col_name_list):
        corr_df = df[col_name_list].corr()
        plt.matshow(corr_df)
        plt.xticks(range(len(corr_df.columns)), corr_df.columns)
        plt.yticks(range(len(corr_df.columns)), corr_df.columns)
        plt.colorbar()
        plt.show()

    def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100):
        formatStr = "{0:." + str(decimals) + "f}"
        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()


class NwpGridAnalyzer:
    def __init__(self):
        self.set_lat_lon_call = 0

        self.lat_grid = None
        self.lon_grid = None

        self.nearest_point = None
        self.nearest_four_grid_point = None

    def set_lat_lon_grid(self, lat_grid, lon_grid):
        self.set_lat_lon_call += 1

        self.lat_grid = lat_grid
        self.lon_grid = lon_grid

    @staticmethod
    def nearest_n_point_weighted_value(grid, distance_index_dic, weighted_type=None):
        numerator = 0
        denominator = 0

        for dis in distance_index_dic:
            val = grid[distance_index_dic[dis][0]][distance_index_dic[dis][1]]/dis
            numerator += val
            denominator += 1/dis

        return numerator/denominator

    def around_four_grid_point(self, lat_given, lon_given):
        lat_total_num = len(self.lat_grid)
        lon_total_num = len(self.lon_grid[0])

        # lat search
        index = lat_total_num // 2
        upper_bound = lat_total_num - 1
        lower_bound = 0

        # lon search function
        def search_lon_based_on_lat(index):
            left_bound = 0
            right_bound = lon_total_num - 1
            comparison_point = lon_total_num // 2

            while 1:
                if lon_given <= self.lon_grid[index][comparison_point]:
                    right_bound = comparison_point
                    comparison_point = int((left_bound + right_bound) // 2)
                elif lon_given > self.lon_grid[index][comparison_point]:
                    left_bound = comparison_point
                    comparison_point = int((left_bound + right_bound) // 2)
                if abs(left_bound - right_bound) == 1:
                    break
            return left_bound, right_bound

        # lat search
        while 1:
            above_of_given_points_condition = 0
            lat_grid = self.lat_grid[index]
            for i, lat_points in enumerate(lat_grid):
                if lat_given <= lat_points:
                    above_of_given_points_condition += 1
                    left_bound, right_bound = search_lon_based_on_lat(index)
                    left_lat, right_lat = lat_grid[left_bound], lat_grid[right_bound]

                    if left_lat <= lat_given and right_lat <= lat_given:
                        lower_bound = index
                        index = (upper_bound + lower_bound) // 2
                        break
                    elif left_lat >= lat_given and right_lat <= lat_given:
                        upper_bound = index
                        index = (upper_bound + lower_bound) // 2
                        break
                    elif left_lat <= lat_given and right_lat >= lat_given:
                        lower_bound = index
                        index = (upper_bound + lower_bound) // 2
                        break
                    else:
                        upper_bound = index
                        index = (upper_bound + lower_bound) // 2
                        break

            if above_of_given_points_condition == 0:
                # left_bound, right_bound = search_lon_based_on_lat(index)
                # left_lat, right_lat = lat_grid[left_bound], lat_grid[right_bound]
                lower_bound = index
                index = (upper_bound + lower_bound)//2
            if upper_bound - lower_bound == 1:
                break

        # lon search
        left_bound, right_bound = search_lon_based_on_lat(lower_bound)

        return upper_bound, lower_bound, left_bound, right_bound

    def nearest_point_index(self, lat_given, lon_given):
        stn_point = (lat_given, lon_given)

        up, low, left, right = self.around_four_grid_point(lat_given, lon_given)
        p1, p2, p3, p4 = (self.lat_grid[up][left], self.lon_grid[up][left]), \
                         (self.lat_grid[up][right], self.lon_grid[up][right]),\
                         (self.lat_grid[low][left], self.lon_grid[low][left]),\
                         (self.lat_grid[low][right], self.lon_grid[low][right])

        d1, d2, d3, d4 = haversine(stn_point, p1), haversine(stn_point, p2), haversine(stn_point, p3), haversine(stn_point, p4)
        dic = {d1: (up, left), d2: (up, right), d3: (low, left), d4: (low, right)}

        nearest_dis = min([d1, d2, d3, d4])
        nearest_point_index = dic[nearest_dis]

        return nearest_point_index

    # exception case should be prepared
    def nearest_n_grid_point(self, lat_given, lon_given, objective_num):
        if int(sqrt(objective_num)) % 2 == 0:
            search_grid_num = int(sqrt(objective_num)) + 2
        else:
            search_grid_num = int(sqrt(objective_num)) + 1

        up, low, left, right = self.around_four_grid_point(lat_given, lon_given)
        move_point = float(search_grid_num/2) - 1
        start_point = [(up+move_point), (left - move_point)]

        all_point_list = []
        for i in range(search_grid_num):
            for j in range(search_grid_num):
                all_point_list.append((start_point[0]-i, start_point[1]+j))

        distance_index_dic = {}
        distance_list = []
        given_point = (lat_given, lon_given)

        for compare_points in all_point_list:
            comp_point_1, comp_point_2 = int(compare_points[0]), int(compare_points[1])
            compare_points = (self.lat_grid[comp_point_1][comp_point_2], self.lon_grid[comp_point_1][comp_point_2])
            compare_index = (comp_point_1, comp_point_2)
            dis_between = haversine(given_point, compare_points)
            distance_index_dic[dis_between] = compare_index
            distance_list.append(dis_between)

        distance_list.sort()
        distance_list = distance_list[:objective_num]

        nearest_point_index_list = []
        for distance_key in distance_list:
            nearest_point_index_list.append(distance_index_dic[distance_key])

        return distance_index_dic, nearest_point_index_list

    def plot_nearest_n_point(self, lat_given, lon_given, objective_num):
        for i in range(len(self.lon_grid)):
            plt.plot(self.lon_grid[i], self.lat_grid[i], "ro", color="green", markersize=0.5)

        _, nearest_n_grid_point = self.nearest_n_grid_point(lat_given, lon_given, objective_num)
        for points in nearest_n_grid_point:
            lat = self.lat_grid[int(points[0])][int(points[1])]
            lon = self.lon_grid[int(points[0])][int(points[1])]
            # plt.plot(points[1], points[0], "ro", color="red")
            plt.plot(lon, lat, "ro", color="red")
        plt.plot(lon_given, lat_given, "ro", color="blue")
        plt.show()

    def plot_nearest_point(self, lat_given, lon_given):
        for i in range(len(self.lon_grid)):
            plt.plot(self.lon_grid[i], self.lat_grid[i], "ro", color="green", markersize=0.5)

        upper_bound, lower_bound, left_bound, right_bound = self.around_four_grid_point(lat_given, lon_given)
        left_upper = [self.lon_grid[upper_bound][left_bound], self.lat_grid[upper_bound][left_bound]]
        left_lower = [self.lon_grid[lower_bound][left_bound], self.lat_grid[lower_bound][left_bound]]
        right_upper = [self.lon_grid[upper_bound][right_bound], self.lat_grid[upper_bound][right_bound]]
        right_lower = [self.lon_grid[lower_bound][right_bound], self.lat_grid[lower_bound][right_bound]]

        plt.plot(left_upper[0], left_upper[1], "ro", color="red")
        plt.plot(left_lower[0], left_lower[1], "ro", color="red")
        plt.plot(right_upper[0], right_upper[1], "ro", color="red")
        plt.plot(right_lower[0], right_lower[1], "ro", color="red")

        plt.plot(lon_given, lat_given, "ro", color="blue")

        plt.show()

    def plot_base_point(self, lat_given, lon_given):
        for i in range(len(self.lon_grid)):
            plt.plot(self.lon_grid[i], self.lat_grid[i], "ro", color="red", markersize=0.3)
            # plt.plot(self.lon_grid[i][:50], self.lat_grid[i][:50], "ro", color="blue")
            # if i > 1:
            #     break
        plt.plot(lon_given, lat_given, "ro", color="blue")
        plt.grid(True)
        plt.show()

