import pandas as pd
import datetime
import re

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
d = [10, 11, 12]
e = [13, 14, 15]

list_of = []
list_of.append(a)
list_of.append(b)
list_of.append(c)
list_of.append(d)
list_of.append(e)

df = pd.DataFrame(list_of, columns=["ga", "sk", "ek"])
df.set_index("ga", inplace=True)


time_interval = ["2019-01-03 00", "2019-01-05 00"]
time_point = ["00", "06", "12", "18"]


def access(time_interval, time_point):
    filename_list = []

    start_time = time_interval[0]
    end_time = time_interval[1]

    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H")

    loop = 0
    while 1:
        loop += 1
        current_time = start_time + datetime.timedelta(days=1*(loop-1))
        if current_time > end_time + datetime.timedelta(days=1):
            break

        re_converted_date_string = re.sub('[^A-Za-z0-9]+', '', str(current_time))[:-6]
        for point in time_point:
            for i in range(36):
                filename = "l015_v070_erlo_unis_h" + str(i).zfill(3) + "." + re_converted_date_string + point + ".gb2"
                filename_list.append(filename)

    return filename_list


access(time_interval, time_point)

