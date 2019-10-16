import os

# paths dependent to local PC
files_path = "/home/jhpark/NWP/"
data_file_path = "/home/jhpark/data_files/"

# paths dependent to the Project
project_root_dir = os.path.dirname(os.path.abspath(__file__))
setting_file_path = os.path.join(project_root_dir,
                                 "data_file/setting_files/")
prediction_input_output_path = os.path.join(project_root_dir,
                                            "data_file/prediction_input_output")
model_path = os.path.join(project_root_dir, "data_file/model_files/")


ldaps_variable_index_file_name = "LDAPS_variables_index_name.xlsx"
rdaps_variable_index_file_name = "RDAPS_variables_index_name.xlsx"

# messages
value_extract_exception_text = "cannot extract values from {} " \
                               "because the file does not exists in local pc"
download_exception_text = "cannot download {} from ftp server " \
                          "because the file does not exists in ftp server"
already_exists_text = "{} already exists in local pc"
runtime_error_text = ": Runtime Error Ocurred with file {}"

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

# mongo db info
mongodb_ip = "10.0.1.40"
mongodb_pw = ""
mongodb_port = 27017

# job control parameter
num_of_process = 3
length_of_time_interval_for_training = 7
