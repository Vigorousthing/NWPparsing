# import datetime
#
#
#
# start_time = "2019-05-04 00"
# compar_time = "2019-05-28 00"
#
# start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
# compar_time = datetime.datetime.strptime(compar_time, "%Y-%m-%d %H")
#
# print(start_time)
#
# print(start_time < compar_time)

import itertools
import re
import datetime

# filename = 'g120_v070_erea_unis_h072.2019072018.gb2'
#
# print(filename[-6:-4])
# print(filename[-17:-15])
# print(filename[-14:-4])
#
# start_time = datetime.datetime.strptime("2019022818", "%Y%m%d%H")
#
# print(start_time)
#
# reconverted = re.sub('[^A-Za-z0-9]+', '', str(start_time))[:-4]
#
# print(reconverted)
#
# a = "dfd{}".format(str(13).zfill(2))
# print(a)
#
#
# for i in range(10):
#     try:
#         1/i
#     except:
#         print("")
#
#
# a = (1,2,3,4,5)
# print(list(list(a)))
#
# b = [[1,2,3,4], [3,4,5,6,7,8]]
#
# print([list(set.union(*map(set, b)))])
#

# a = datetime.datetime.now()
#
# print(eval(a.__repr__()))
#
# y = str(a.year)
# m = str(a.month)
# d = str(a.day)
# h = str(a.hour)
# s = str(a.second)
# print(y+m+d+h+s)


current_time = datetime.datetime.strptime("2019-08-08 15", "%Y-%m-%d %H")
nearest_prediction_time = datetime.datetime.strptime("2019-08-07 20", "%Y-%m-%d %H")

# print((current_time - nearest_prediction_time).days)

if current_time.hour >= nearest_prediction_time.hour:
    hour_dif_from_prediction_time = current_time.hour - nearest_prediction_time.hour
    day_dif_from_prediction_time = (current_time - nearest_prediction_time).days
    hour_converted_time_dif = hour_dif_from_prediction_time + day_dif_from_prediction_time * 24
else:
    hour_dif_from_prediction_time = current_time.hour + (24 - nearest_prediction_time.hour)
    day_dif_from_prediction_time = (current_time - nearest_prediction_time).days
    hour_converted_time_dif = hour_dif_from_prediction_time + day_dif_from_prediction_time * 24

print(hour_converted_time_dif)