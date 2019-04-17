import ftp_CONSTANT
import CONSTANT
import netCDF4
from nwp_parsing import *

##################################################################################################
ip = ftp_CONSTANT.ftp_ip
id, pw = ftp_CONSTANT.ftp_id, ftp_CONSTANT.ftp_pw
local_path = ftp_CONSTANT.local_path
##################################################################################################
'''
input category
data_type : LDAPS / RDAPS / SATELLITE / AWS / ASOS
fold_type : unis / pres
nearest_type = 1 / "n"

example of inputs of functions
time_interval = ["2019-03-04 00", "2019-04-05 00"]
horizontal_interval = [12, 24]
time_point = ["00", "12", "18"]
point = (36, 128)
'''

data_type = "LDAPS"
fold_type = "unis"
time_interval = ["2019-02-04 00", "2019-04-05 00"]
horizon_interval = [0, 12]

var_list = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]
nearest_type = 1

point = (37.57142, 126.9658)

ftp_accessor = FtpAccess(ip, id, pw)

# print CONSTANT.now_str

"before_setting function"
# ftp_accessor.check_file_size(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
# ftp_accessor.file_save(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
# ftp_accessor.variable_extractor(data_type, fold_type, time_interval, horizon_interval=horizon_interval)

"after setting function"
ftp_accessor.data_type_setting(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
ftp_accessor.set_file_names()
# ftp_accessor.check_total_size_of_files()
# ftp_accessor.save_file_from_ftp_server()
# ftp_accessor.extract_variable_values_from_saved_files()

# ftp_accessor.close()
##################################################################################################




if __name__ == "__main__":
    nwp_file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h004.2019032400.gb2")
    lat_grid, lon_grid = nwp_file[4].latlons()
    point = (37.57142, 126.9658)

    analyzer = NwpGridAnalyze()
    # analyzer.set_lat_lon_grid(lat_grid, lon_grid)
    # analyzer.plot_base_point(lat_point, lon_point, lat, lon)
    # analyzer.plot_nearest_point(analyzer.around_four_grid_point(point[0], point[1]), point[0], point[1])
    # analyzer.plot_nearest_n_point(analyzer.nearest_n_grid_point(10, point[0], point[1]), point[0], point[1])

<<<<<<< HEAD

"do you think this will be changed?"
=======
"this plus"
>>>>>>> experiment
