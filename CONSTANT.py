import os

# data manipulation constant
subtract_for_prediction_df = ["CRTN_TM", "horizon", "FCST_TM", "lat", "lon",
                              "location_num"]

# paths dependent to local PC

files_path = "/home/jhpark/NWP/"
data_file_path = "/home/jhpark/data_files/"

# paths dependent to the Project
project_root_dir = os.path.dirname(__file__)
setting_file_path = os.path.join(project_root_dir,
                                 "data_file/setting_files/")
prediction_input_output_path = os.path.join(project_root_dir,
                                            "data_file/prediction_input_output")
model_path = os.path.join(project_root_dir, "data_file/model_files/")

ldaps_variable_index_file_name = "LDAPS_variables_index_name.xlsx"
rdaps_variable_index_file_name = "RDAPS_variables_index_name.xlsx"

var_by_model_file_name = "var_by_model_info.xlsx"

# messages
value_extract_exception_text = "cannot extract values from {} " \
                               "because the file does not exists in local pc"
download_exception_text = "cannot download {} from ftp server " \
                          "because the file does not exists in ftp server"
already_exists_text = "{} already exists in local pc"
runtime_error_text = ": Runtime Error Ocurred with file {}"
ldaps_not_found_text = "cannot predict with ldaps file. fcst_tm: {}, " \
                       "lead_tm: {}"

# ftp info
ftp_ip = "10.0.0.3"
ftp_id, ftp_pw = "kmiti", "kmadataset!"
ftp_ROOT = "/"

# sql db info
db_ip_jeju = "kyonsu.sun-wms.com"
db_ip_nonsan_gayagok1 = "yj3.sun-wms.com"
db_ip_nonsan_yujin2 = "yj2.sun-wms.com"

db_id = "wmudb"
db_pw = "xodidrhkd2020"

db_name = "rtu"

# goduk / dobong / jichuk / gaehwa
# capacity : 612 / 648 / 1992 / 990
garage_coordinates = [(37.566601, 127.168451), (37.701720, 127.052289),
                      (37.651369, 126.906272), (37.578967, 126.793614)]

# jeju / nonsan
jenon_coordinates = [(33.2875, 126.648611), (36.149019, 127.176031)]


# mongo db info
mongodb_ip = "10.0.1.40"
mongodb_pw = ""
mongodb_port = 27017

# job control parameter
num_of_process = 3
length_of_time_interval_for_training = 7
limit_goal_of_prediction_interval = 48
