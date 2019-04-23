import os
import re
import ftplib
import pygrib
import datetime
from math import *
import pandas as pd
from haversine import *
import matplotlib.pyplot as plt


class FtpAccess:
    def __init__(self, ip, id, pw):
        self.ftp = ftplib.FTP()
        self.ftp.connect(ip)
        self.ftp.login(id, pw)

        self.data_type = None
        self.fold_type = None
        self.time_interval = None
        self.time_point = None

        self.file_name_list = []

        self.nearest_file_list = []

        self.local_path = "/home/jhpark/NWP"

    def data_type_setting(self, data_type, fold_type, time_interval, horizon_interval=[0, 36], time_point=["00", "06", "12", "18"]):
        self.data_type = data_type
        self.fold_type = fold_type
        self.time_interval = time_interval
        self.horizon_interval = horizon_interval
        self.time_point = time_point

        current_dir = "/" + data_type
        self.ftp.cwd(current_dir)

    def local_path_setting(self, local_path="/home/jhpark/NWP"):
        self.local_path = local_path

    def set_file_names(self):
        dir_dic = {"RDAPS": "g120", "LDAPS": "l015", "SATELLIE": None, "AWS": None, "ASOS": None}

        self.file_name_list = []

        start_time = self.time_interval[0]
        end_time = self.time_interval[1]

        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H")

        # UTC correction
        start_time = start_time - datetime.timedelta(hours=9)
        end_time = end_time - datetime.timedelta(hours=9)

        print "after conversion", start_time

        number_of_horizon = self.horizon_interval[1] - self.horizon_interval[0] + 1

        # start / end time alignment for prediction time
        if start_time.hour % 6 != 0:
            start_time = start_time + datetime.timedelta(hours=(6 - (start_time.hour % 6)))
        if end_time.hour % 6 != 0:
            end_time = end_time - datetime.timedelta(hours=end_time.hour % 6)

        # time interval between at each given time points(subset of [00, 06, 12, 18])
        time_interval = []
        for i, val in enumerate(self.time_point):
            if i + 1 == len(self.time_point):
                time_interval.append(int(self.time_point[((i + 1) % len(self.time_point))]) + 24 - int(val))
                break
            else:
                time_interval.append(int(self.time_point[i+1]) - int(val))

        current_index_for_time_interval = self.time_point.index(str(start_time.hour).zfill(2))

        current_time = start_time

        time_interval_length = len(time_interval)
        while 1:
            re_converted_date_string = re.sub('[^A-Za-z0-9]+', '', str(current_time))[:-6]
            for i in range(number_of_horizon):
                filename = dir_dic[self.data_type] + "_v070_erlo_" + self.fold_type + "_h" + str(self.horizon_interval[0] + i).zfill(3) + "." + \
                           re_converted_date_string + str(current_time.hour).zfill(2) + ".gb2"
                self.file_name_list.append(filename)

            current_time = current_time + datetime.timedelta(hours=time_interval[current_index_for_time_interval % time_interval_length])

            if current_time > end_time:
                break

            current_index_for_time_interval += 1

    def check_total_size_of_files(self):
        file_size = 0
        file_num = 0
        for file_name in self.file_name_list:
            try:
                file_size += self.ftp.size(file_name)
                file_num += 1
            except ftplib.error_perm:
                print file_name + " not exists in ftp server"
        print "total size of files : ", float(file_size)/(1024*1024*1024), "gb", ", total number of files :", file_num

    def save_file_from_ftp_server(self):
        for filename in self.file_name_list:
            try:
                path = os.path.join(self.local_path, filename)
                if os.path.exists(path):
                    print filename + " already exists in local pc"
                    continue
                new_file = open(path, "wb")
                self.ftp.retrbinary("RETR " + filename, new_file.write)
                new_file.close()
            except ftplib.error_perm:
                os.remove(path)
                print "cannot download " + filename + " from ftp server because the file does not exists in ftp server"

    def extract_variable_values_from_saved_files(self, nwp_var_list, nearest_type, given_point, output_file_name="new"):
        # set analyzer
        nwp_grid_analyzer = NwpGridAnalyze()

        path = os.path.join(self.local_path, self.file_name_list[0])
        temp_file = pygrib.open(path)
        lat_grid, lon_grid = temp_file[1].latlons()
        nwp_grid_analyzer.set_lat_lon_grid(lat_grid, lon_grid)
        temp_file.close()

        # make var index dic
        nwp_var_index_dic = pd.read_excel("LDAPS_variables_index_name.xlsx").set_index("var_abbrev")["index"]

        # make column list
        col = ["CRTN_TM", "horizon", "FCST_TM"]
        for var in nwp_var_list:
            col.append(var)

        # set dataframe
        df = pd.DataFrame(columns=col)

        # add rows to dataframe
        for filename in self.file_name_list:
            path = os.path.join(self.local_path, filename)
            horizon = int(filename.split("h")[1].split(".")[0])
            # utc correction included in crtn_tm
            crtn_tm = datetime.datetime.strptime(filename.split("h")[1].split(".")[1], "%Y%m%d%H") + datetime.timedelta(hours=9)
            fcst_tm = crtn_tm + datetime.timedelta(hours=horizon)

            row = [crtn_tm, horizon, fcst_tm]

            if os.path.exists(path) is False:
                print "cannot extract values from " + filename + " because the file does not exists in local pc"
                continue
            else:
                nwp_file = pygrib.open(path)
                for var_name in col:
                    if var_name == "CRTN_TM" or var_name == "horizon" or var_name == "FCST_TM":
                        continue
                    # extract variable index
                    index = nwp_var_index_dic[var_name].item()
                    if nearest_type == 1:
                        # make grid data - by nearest_type
                        # 1) load grid value data
                        var_grid_values = nwp_file[index].values
                        # 2) get grid indexes
                        nearest_point_index = nwp_grid_analyzer.nearest_point_index(given_point[0], given_point[1])
                        # 3) get value by index from grid
                        value = var_grid_values[nearest_point_index[0]][nearest_point_index[1]]
                    elif nearest_type == "n":
                        # make grid data - by nearest_n_type
                        # 1) load grid value data
                        var_grid_values = nwp_file[index].values
                        # 2) make dis_index_dic for n-nearest points
                        nearest_point_dis_index_dic, _ = nwp_grid_analyzer.nearest_n_grid_point(4, given_point[0], given_point[1])
                        # 3) interpolate values from n-nearest points
                        value = nwp_grid_analyzer.nearest_n_point_weighted_value(var_grid_values, nearest_point_dis_index_dic)
                    row.append(value)
                nwp_file.close()
            row = pd.Series(row, index=col)
            df = df.append(row, ignore_index=True)

        df.to_pickle("/home/jhpark/experiment_files/" + output_file_name + ".pkl")
        df.to_excel("/home/jhpark/experiment_files/" + output_file_name + ".xlsx")

        print df

    def remove_from_local_pc(self):
        for filename in self.file_name_list:
            path = os.path.join(self.local_path, filename)
            if os.path.exists(path):
                os.remove(path)
            else:
                print "cannot remove " + filename + " because the file does not exists in local pc"

    def find_nearest_nwp_prediction_file_in_local(self, current_time, horizon_num):
        """
        this function intends to find latest nwp prediction file towards each time horizon from current time
        if local file system does not have a such file, then missing value should be interpolated
        """
        # number_of_horizon = self.horizon_interval[1] - self.horizon_interval[0] + 1

        # data type and filename part pair
        dir_dic = {"RDAPS": "g120", "LDAPS": "l015", "SATELLIE": None, "AWS": None, "ASOS": None}

        # length of time horizon
        horizon_num = horizon_num + 1

        # from korean time to UTC time(NWP notation)
        current_time = current_time - datetime.timedelta(hours=9)

        file_name_list = []
        for i in range(horizon_num):
            "loop for every time horizon"
            # distance from latest prediction time
            dif = current_time.hour % 6

            while 1:
                "find nearest file"

                nearest_prediction_time = current_time - datetime.timedelta(hours=dif)
                re_converted_date_string = re.sub('[^A-Za-z0-9]+', '', str(nearest_prediction_time))[:8]

                hour_dif_from_prediction_time = (current_time - nearest_prediction_time).seconds/3600

                filename = dir_dic[self.data_type] + "_v070_erlo_" + self.fold_type + "_h" + str(hour_dif_from_prediction_time + i).zfill(3) + "." + \
                           re_converted_date_string + str(nearest_prediction_time.hour).zfill(2) + ".gb2"

                path = os.path.join(self.local_path, filename)

                if os.path.exists(path) and (str(nearest_prediction_time.hour).zfill(2) in self.time_point):
                    file_name_list.append(filename)
                    break
                elif abs((current_time - nearest_prediction_time).days) >= 2:
                    file_name_list.append(None)
                    print "no matched file in recent 2 days"
                    break
                else:
                    dif += 6

        self.nearest_file_list = file_name_list
        return file_name_list

    def close(self):
        self.ftp.quit()


class NwpGridAnalyze:
    def __init__(self):
        self.lat_grid = None
        self.lon_grid = None

        self.nearest_point = None
        self.nearest_four_grid_point = None

    def set_lat_lon_grid(self, lat_grid, lon_grid):
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
    def nearest_n_grid_point(self, objective_num, lat_given, lon_given):
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

        # lon search
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
                left_bound, right_bound = search_lon_based_on_lat(index)
                # left_lat, right_lat = lat_grid[left_bound], lat_grid[right_bound]
                lower_bound = index
                index = (upper_bound + lower_bound)//2
            if upper_bound - lower_bound == 1:
                break

        # lon search
        left_bound, right_bound = search_lon_based_on_lat(lower_bound)

        return upper_bound, lower_bound, left_bound, right_bound

    def plot_nearest_n_point(self, nearest_n_grid_point, lat_given, lon_given):
        _, nearest_n_grid_point = nearest_n_grid_point
        for points in nearest_n_grid_point:
            lat = self.lat_grid[int(points[0])][int(points[1])]
            lon = self.lon_grid[int(points[0])][int(points[1])]
            # plt.plot(points[1], points[0], "ro", color="red")
            plt.plot(lon, lat, "ro", color="red")
        plt.plot(lon_given, lat_given, "ro", color="blue")
        plt.show()

    def plot_nearest_point(self, around_four_grid_point, lat_given, lon_given):
        upper_bound, lower_bound, left_bound, right_bound = around_four_grid_point
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
            plt.plot(self.lon_grid[i], self.lat_grid[i], "ro", color="green")
            # plt.plot(self.lon_grid[i][:50], self.lat_grid[i][:50], "ro", color="blue")
            # if i > 1:
            #     break
        plt.plot(lon_given, lat_given, "ro", color="red")
        plt.grid(True)
        plt.show()
