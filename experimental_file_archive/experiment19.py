import os

# a = os.path.exists("/home/jhpark/NWP/g120_v070_erea_unis_h042.2019050412.gb2")
# b = os.path.exists("/home/jhpark/NWP/g120_v070_erea_unis_h081.2019050412.gb2")
# print(a)
# print(b)

# try:
#     a = 1
#     b = 0
#     c = a/b
#
# except BaseException:
#     print("123123")
# else:
#     print("go further")
# finally:
#     print("finally here")
#
#
# print("outside block")

# a = "the old oak tree in my town stands magnificently"
#
#
# def index_words_iter(text):
#     if text:
#         yield 0
#     for index, letter in enumerate(text):
#         if letter == " ":
#             yield index + 1
#
#
# b = index_words_iter(a)
#
# print(list(b))


# class A:
#     def __init__(self):
#         pass
#
#     @classmethod
#     def new(cls, a, b):
#         pass
#

# import nwp_parsing
# import pandas as pd
#
# visualizer = nwp_parsing.Visualizer()
# # df = pd.read_excel("/home/jhpark/experiment_files/nwp_and_real_corr2.xlsx")
# df = pd.read_excel("/home/jhpark/experiment_files/real_weather_corr.xlsx")
#
# # visualizer.correlation_matrix(df, ["real", "NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS", "UGRD", "VGRD", "TMP", "SPFH", "RH", "DPT"])
# visualizer.correlation_matrix(df, ["real", "TMP", "WS", "WD", "HD", "DPT", "AP", "total_cloud", "intemp", "outtemp", "IRR"])
#
# import datetime
# import re
#
# start_time = "2019-04-05 11"
# start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H")
# date_string = re.sub('[^A-Za-z0-9]+', '', str(start_time))[:-4]
# print(date_string)
#
# a = "2019050618"
# a = datetime.datetime.strptime(a, "%Y%m%d%H")
# print(a)


class A:
    horizon = 1

    def __init__(self, a, b, c):
        self.set_pro(a,b,c)

    def set_pro(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def upper(self):
        print(self.horizon)
        def inner():
            print(self.a)
        inner()

class B(A):
    horizon=101
    def __init__(self,a,b,c):
        super(B, self).__init__(a,b,c)
        print("B instance created")
        pass

# a,b,c = "heelo","printamy",33333
# d = B(a, b, c)
# e = B(33, 44, 55)
# # d.set_pro(a,b,c)
#
# print(d.a, d.b, d.c)
# print(e.a, e.b, e.c)


# a = A(100,2,3)
# a.upper()


print([0 for i in range(10)])
