import ftp_CONSTANT
from nwp_parsing import *

ip = ftp_CONSTANT.ftp_ip
id, pw = ftp_CONSTANT.ftp_id, ftp_CONSTANT.ftp_pw
local_path = ftp_CONSTANT.local_path
nwp_file_handler = NwpFileHandler(ip, id, pw)

data_type = "RDAPS"
fold_type = "unis"

time_interval = ["2019-07-21 00", "2019-07-28 23"]
time_interval = ["2019-07-21 00", "2019-07-21 07"]

horizon_interval = [0, 87]
time_point = ["00", "09", "12", "18"]
# var_list = ["NDNSW", "INSWT", "OUSWT", "CUSWT", "CDSWS", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "NDLWO", "OULWT", "CULWT", "DLWS", "CDLWS"]
var_list = ["TDSWS", "UGRD", "VGRD", "TMP", "SPFH", "RH", "DPT"]

nearest_type = 1
point = [(37.566601, 127.168451), (37.701720, 127.052289), (37.651369, 126.906272), (37.578967, 126.793614)]
current_time = datetime.datetime.strptime("2019-05-08 10", "%Y-%m-%d %H")


ftp_accessor = NwpFileHandler(ip, id, pw, True)
ftp_accessor.set_for_files(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
ftp_accessor.set_for_values(var_list, nearest_type, point)
ftp_accessor.set_file_names()
ftp_accessor.save_file_from_ftp_server()

# df = ftp_accessor.extract_variable_values()

# df.to_excel("/home/jhpark/experiment_files/forRDAPS0721to0728.xlsx")

# ftp_accessor.save_target_file("RDAPS", "g120_v070_erea_unis_h087.2019072018.gb2")
