import datetime

a = datetime.datetime.now().replace(microsecond=0)
b = datetime.datetime.now().replace(microsecond=0)

print(int((b-a).total_seconds()))
