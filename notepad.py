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
