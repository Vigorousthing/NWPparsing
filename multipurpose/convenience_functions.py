import pandas as pd
import re

point = [(37.38916, 127.62097), (37.36872, 127.64302), (34.59612, 126.29099), (36.17202, 126.78948), (37.10368, 128.24847)]


data = pd.read_excel("vpp_info.xlsx")
data = data.set_index("site")
data = data.drop("capacity", axis=1)
dic = data.to_dict()["Coordinates"]

site_name_list = []
print(dic)
for key in dic:
    site_name_list.append(dic[key])
print(site_name_list)
# site_name_list = []
# for i in point:
#     site_name_list.append(dic[str(i)])
# print site_name_list

def site_id_to_coordinate(site_name_list):
    coordinate_list = []
    data = pd.read_excel("vpp_info.xlsx")
    data = data.set_index("site")
    data = data.drop("capacity", axis=1)
    dic = data.to_dict()["Coordinates"]

    if site_name_list == None:
        for key in dic:
            coordinate_list.append(dic[key])
    else:
        for site_name in site_name_list:
            coordinate_list.append(dic[site_name])
    return coordinate_list


def coordinate_to_site_id(coordinate_list):
    if coordinate_list == None:
        site_name_list = None
    else:
        data = pd.read_excel("vpp_info.xlsx")
        data = data.set_index("Coordinates")
        data = data.drop("capacity", axis=1)
        dic = data.to_dict()["site"]
        site_name_list = []
        for coordinate in coordinate_list:
            site_name_list.append(dic[str(coordinate)])
    return site_name_list