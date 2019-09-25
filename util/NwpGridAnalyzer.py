import matplotlib.pyplot as plt
from haversine import haversine
from math import sqrt


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
