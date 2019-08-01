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
i = 0
while 1:
    i += 1
    try:
        1/0
    except:
        print("1")

    if i > 100:
        break
