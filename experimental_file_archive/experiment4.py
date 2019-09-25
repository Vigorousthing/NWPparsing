from Load_data import *
from data_manipulation import *

# temp_file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h015.2019031212.gb2")
# a = temp_file[1].values
# print(a)

from legacy.nwp_parsing import *

grid_analyzer = NwpGridAnalyzer()

filename = 'g120_v070_erea_unis_h033.2019072612.gb2'

full_path = "/home/jhpark/NWP/g120_v070_erea_unis_h063.2019080100.gb2"
# nwp_file = pygrib.open("/home/jhpark/NWP/" + filename)
nwp_file = pygrib.open(full_path)

# for i, val in enumerate(nwp_file):
#     print(nwp_file[i+1])

lat_grid, lon_grid = nwp_file[1].latlons()
grid_analyzer.set_lat_lon_grid(lat_grid, lon_grid)

given_point = (34.576936, 126.436539)
given_point = (32, 158.356)

# grid_analyzer.plot_nearest_point(grid_analyzer.around_four_grid_point(given_point[0], given_point[1]), given_point[0], given_point[1])
grid_analyzer.plot_nearest_point(given_point[0], given_point[1])


a = [{1,2,3,4,5}, {2,3,4,5,6,7}, {10,11,12,13}]

print(set.union(*a))