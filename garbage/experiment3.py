import os
import CONSTANT
path = "/home/jhpark/NWP/l015_v070_erlo_pres_h000.2019032112.gbd"
# nf = open(path)

print os.path.exists(path)

for i in range(10):
    try:
        if os.path.exists(path):
            print "exists"
        else:
            continue
    except BaseException:
        pass
    print i


import datetime

time_interval = ["2019-03-04 00", "2019-04-05 00"]
start_time = time_interval[0]
end_time = time_interval[1]

start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H")

start_time = start_time - datetime.timedelta(hours=9)
end_time = end_time - datetime.timedelta(hours=9)


print start_time, end_time

day_str = str(datetime.datetime.now().date())
hour_str = str(datetime.datetime.now().hour)
time_str = day_str + " " + hour_str


std_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H")

dif = std_time.hour % 6

nearest_time = std_time - datetime.timedelta(hours=dif)
scn_nearest_time = nearest_time - datetime.timedelta(hours=6)
trd_nearest_time = scn_nearest_time - datetime.timedelta(hours=6)

print nearest_time

print str(nearest_time.hour).zfill(2)


current_time = datetime.datetime.strptime(CONSTANT.now_str, "%Y-%m-%d %H")

# find_nearest_nwp_prediction(current_time)

