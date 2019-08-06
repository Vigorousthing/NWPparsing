import ftp_CONSTANT
from nwp_parsing import *

ip = ftp_CONSTANT.ftp_ip
id, pw = ftp_CONSTANT.ftp_id, ftp_CONSTANT.ftp_pw
local_path = ftp_CONSTANT.local_path
nwp_file_handler = NwpFileHandler(ip, id, pw)

data_type = "RDAPS"
fold_type = "unis"

# time_interval = ["2019-06-01 00", "2019-06-10 23"]
# time_interval = ["2019-06-11 00", "2019-06-20 23"]
time_interval = ["2019-06-21 00", "2019-06-30 23"]

horizon_interval = [0, 87]
time_point = ["00", "09", "12", "18"]
# var_list = ["NDNSW", "INSWT", "OUSWT", "CUSWT", "CDSWS", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "NDLWO", "OULWT", "CULWT", "DLWS", "CDLWS"]
var_list = ["TDSWS", "UGRD", "VGRD", "TMP", "SPFH", "RH", "DPT"]

nearest_type = 1

# four garage coordinates
# test_point = [(37.566601, 127.168451), (37.701720, 127.052289), (37.651369, 126.906272), (37.578967, 126.793614)]

# training points
# corresponding to hwangsan myun office, ASOS station, big solar plant
training_point = [(34.576936, 126.436539), (34.55375, 126.56907), (34.549625, 126.438429)]

# current_time = datetime.datetime.strptime("2019-05-08 10", "%Y-%m-%d %H")

ftp_accessor = NwpFileHandler(ip, id, pw, True)
ftp_accessor.set_for_files(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
ftp_accessor.set_for_values(var_list, nearest_type, training_point)
ftp_accessor.set_file_names()
ftp_accessor.save_file_from_ftp_server()
df = ftp_accessor.extract_variable_values()

print("exp1 check")
# df.to_excel("/home/jhpark/experiment_files/forRDAPStraining0601to0610.xlsx")
