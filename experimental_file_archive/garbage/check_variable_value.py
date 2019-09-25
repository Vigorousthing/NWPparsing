import pygrib

file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h000.2019042612.gb2")

double_list = file[118].values

for i in double_list:
    print(i)