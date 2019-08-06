import haversine
from xlrd import open_workbook
from decimal import Decimal
# def nearest_point(given_point, latlon_list, latlon_dic):
#     min_point_dis = 30000
#     min_point_name = None
#     min_point = None
#     for latlon in latlon_list:
#         dis_between = haversine.haversine(given_point, latlon)
#         if dis_between < min_point_dis:
#             min_point = latlon
#             min_point_name = latlon_dic[min_point]
#             min_point_dis = dis_between
#     return min_point_name, min_point, min_point_dis

def nearest_point(given_point, latlon_list):
    min_point_dis = 30000
    min_point_name = None
    min_point = None
    for latlon in latlon_list:
        dis_between = haversine.haversine(given_point, latlon)
        if dis_between < min_point_dis:
            min_point = latlon
            min_point_dis = dis_between
    return min_point_name, min_point, min_point_dis


book = open_workbook("vpp_info.xlsx")
sheet = book.sheet_by_index(0)

latlon_list = []
# latlon_dic = {}
for row_num in range(sheet.nrows):
    coordinate = (sheet.row_values(row_num)[2], sheet.row_values(row_num)[3])
    latlon_list.append(coordinate)
    # latlon_dic[coordinate] = sheet.row_values(row_num)[0]

given_point = (35.832973, 127.120376)
print(nearest_point(given_point, latlon_list))
