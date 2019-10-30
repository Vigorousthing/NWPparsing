from data_accessors.FtpAccessor import FtpAccessor
from nwp_object.FilesContainer import FilesContainer
from nwp_object.NwpFile import *
from util.input_converter import *
import CONSTANT
import time


# time_interval = [2019080100, 2019091000]
# time_interval = InputConverter().time_interval_conversion(time_interval)
#
# accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id,
#                                         CONSTANT.ftp_pw)
# container = FilesContainer(LdapsFile, "unis", [(33.2875, 126.648611)],
#                            ["NDNSW"])
# container.generate_base_files(time_interval)
#
# filename = "l015_v070_erlo_unis_h002.2019042306.gb2"
# result = accessor.existence_check(filename)
# print(result)

# container = FilesContainer(LdapsFile, "unis", [(33.2875, 126.648611)],
#                            ["NDNSW"])
# container.generate_real_time_prediction_files(accessor)
#
# print(container.filename_list)
# print(len(container.filename_list))

# import CONSTANT
# import pandas as pd
# a = pd.read_excel(CONSTANT.data_file_path + "before_refactor_df.xlsx")
# b = pd.read_excel(CONSTANT.data_file_path + "after_refactor_df.xlsx")
# c = a.equals(b)
# print(c)


def decorator(func):
    print("wow")

    def deco(*args):
        print(*args)

    # print(func)

    # return deco


@decorator
def original_func(a, b):
    print("original", a, b)


class TestClass:
    def __init__(self):
        print("start")

    @classmethod
    def ab(cls):
        print("classmethoduse")



def a(a):
    print("start")

def b(a):
    a(a)

def c(a):
    b(a)

def d(a):
    c(a)

def e(a):
    d(a)

def f(a):
    e(a)

f(1)