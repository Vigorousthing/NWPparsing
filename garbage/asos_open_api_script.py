import pandas as pd
from bs4 import BeautifulSoup
import requests
import httplib
import json
import pandas as pd
import re

url = 'http://data.kma.go.kr/apiData/getData?' \
      'type=json&' \
      'dataCd=ASOS&' \
      'dateCd=HR&' \
      'startDt=20180604&' \
      'startHh=07&' \
      'endDt=20180610&' \
      'endHh=09&' \
      'stnIds=108&' \
      'schListCnt=50&' \
      'pageIndex=3&' \
      'apiKey=X5IjNivnxh1NCZBzPun%2BZUWzh5Ah5d8uC57ogn4YcVxgMOAq0TAm2ruOVC7XjH8v'

# res = requests.get(url, verify=False)
# print res.json()
# print res.json()[3]["info"]
#
# js = pd.DataFrame(res.json()[3]["info"])
# print js



# print type(res.json())
#
# js = js.append(None)

# js = js[["TM", "ICSR", "ts"]]
# print js

# js["ICSR"] = js["ICSR"]*278
# print js

time_interval = ["2019-04-25 18", "2019-04-26 00"]


# start_date = re.sub('[^A-Za-z0-9]+', '', str(time_interval[0]))
# end_date = re.sub('[^A-Za-z0-9]+', '', str(time_interval[1]))
# startDt = start_date[:-2]
# startHh = start_date[-2:]
# endDt = end_date[:-2]
# endHh = end_date[-2:]
# print startDt, startHh, endDt, endHh

def open_api(time_interval, station_num):
    start_date = re.sub('[^A-Za-z0-9]+', '', str(time_interval[0]))
    end_date = re.sub('[^A-Za-z0-9]+', '', str(time_interval[1]))

    startDt = start_date[:-2]
    startHh = start_date[-2:]
    endDt = end_date[:-2]
    endHh = end_date[-2:]

    df = None
    i = 0
    while 1:
        i += 1
        url = 'http://data.kma.go.kr/apiData/getData?' \
              'type=json&' \
              'dataCd=ASOS&' \
              'dateCd=HR&' \
              'startDt={}&' \
              'startHh={}&' \
              'endDt={}&' \
              'endHh={}&' \
              'stnIds={}&' \
              'schListCnt={}&' \
              'pageIndex={}&' \
              'apiKey=X5IjNivnxh1NCZBzPun%2BZUWzh5Ah5d8uC57ogn4YcVxgMOAq0TAm2ruOVC7XjH8v'
        url = url.format(startDt, startHh, endDt, endHh, station_num, 999, i)

        res = requests.get(url, verify=False)

        num = 999
        if res.json()[1]["msg"] != "success":
            url = url.format(startDt, startHh, endDt, endHh, station_num, num, 1)
            print requests.get(url, verify=False).json()
            break

        mem = df
        df = pd.DataFrame(res.json()[3]["info"])
        df = df.append(mem)

        # js["ICSR"] = js["ICSR"] * 278
    print df

open_api(time_interval, 108)

