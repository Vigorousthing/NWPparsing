import datetime

current_time = "2019-04-10 19"
current_time = datetime.datetime.strptime(current_time, "%Y-%m-%d %H")

current_time2 = "2019-04-09 10"
current_time2 = datetime.datetime.strptime(current_time2, "%Y-%m-%d %H")

dif = current_time - current_time2

print(dif)
day = dif.days
hour = int(dif.seconds/3600)

# print(int(dif.seconds/3600))

print(day, hour)