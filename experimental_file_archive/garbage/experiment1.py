import pygrib
import pandas as pd
from legacy import nwp_parsing

# a = pygrib.open("/home/jhpark/PycharmProjects/NWPparsing/l015_v070_erlo_unis_h035.2019030806.gb2")
# a = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h012.2019031200.gb2")
a = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h003.2019031900.gb2")
b = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h004.2019032400.gb2")

c, d = a[4].latlons()


# for i in range(100):
#     print np.array_equal(c, b[i+1].latlons())

# print type(a)
# for i in a:
#     print i
    # print str(i)[:str(i).index(":")]
    # print str(i).split(":")[0]
    # print str(i)
    # print i.values

# max_temp = a.select(name="Maximum temperature")[0]
# # uwc = a.select(name="")[0]
# print type(max_temp)
data = pd.read_excel("LDAPS_variables_index_name.xlsx")
data = data.set_index("var_abbrev")

nwp_var_index_dic = data["index"]
# var_list = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]
var_list = ["TDSWS"]


# def variables_extract(nwp_object, var_index_dic, var_list):
#     for var in var_list:
#         index = var_index_dic[var].item()
#         nwp_data = nwp_object[index].values
#         # print nwp_data
#         for i, val in enumerate(nwp_data):
#             if i > 400 and i<500:
#                 # print i, len(val)
#                 # print val
#                 pass

analyzer = nwp_parsing.NwpGridAnalyze()

lat_grid, lon_grid = a[4].latlons()

analyzer.set_lat_lon_grid(lat_grid, lon_grid)
analyzer.plot_base_point(40, 130)


# variables_extract(a, nwp_var_index_dic, var_list)




# print a[8].values

# sw_flux = a.select(name="Net down surface SW flux")[0]

# data = max_temp.values
# lats, lons = max_temp.latlons()

# print lats, lons
# print data.shape
# print data.min()
# print data.max()
# print data
# print feature.dataDate

# ar_np = np.array(data)
# print ar_np


# the_count = [1, 2, 3, 4, 5]
# for number in the_count:
#     print(str(number).zfill(3))

