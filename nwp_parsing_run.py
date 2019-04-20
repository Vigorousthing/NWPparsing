import ftp_CONSTANT
from nwp_parsing import *
import nwp_parsing_controller
##################################################################################################
ip = ftp_CONSTANT.ftp_ip
id, pw = ftp_CONSTANT.ftp_id, ftp_CONSTANT.ftp_pw
local_path = ftp_CONSTANT.local_path
ftp_accessor = FtpAccess(ip, id, pw)
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
# time_interval = ["2019-03-04 00", "2019-04-05 00"]
time_interval = ["2019-04-06 00", "2019-04-15 00"]
horizon_interval = [0, 12]
var_list = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]
nearest_type = 1
point = (37.57142, 126.9658)
current_time = datetime.datetime.now()


# nwp_parsing_controller.extract_variable_values(ftp_accessor, data_type, fold_type, time_interval,
#                                                var_list, nearest_type, point,
#                                                output_file_name="experimental",
#                                                horizon_interval=horizon_interval)
#
# nwp_parsing_controller.remove_files(ftp_accessor, data_type, fold_type, time_interval, horizon_interval=horizon_interval)
ftp_accessor.data_type_setting(data_type, fold_type, time_interval, horizon_interval)
print current_time-datetime.timedelta(days=11)
print ftp_accessor.find_nearest_nwp_prediction_file_in_local(current_time-datetime.timedelta(days=11))


##################################################################################################



if __name__ == "__main__":
    # nwp_file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h004.2019032400.gb2")
    # lat_grid, lon_grid = nwp_file[4].latlons()
    # point = (37.57142, 126.9658)
    #
    # analyzer = NwpGridAnalyze()
    # analyzer.set_lat_lon_grid(lat_grid, lon_grid)
    # analyzer.plot_base_point(lat_point, lon_point, lat, lon)
    # analyzer.plot_nearest_point(analyzer.around_four_grid_point(point[0], point[1]), point[0], point[1])
    # analyzer.plot_nearest_n_point(analyzer.nearest_n_grid_point(10, point[0], point[1]), point[0], point[1])
    pass

