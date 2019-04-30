import ftp_CONSTANT
from nwp_parsing import *
import pickle
import nwp_parsing_controller
##################################################################################################
ip = ftp_CONSTANT.ftp_ip
id, pw = ftp_CONSTANT.ftp_id, ftp_CONSTANT.ftp_pw
local_path = ftp_CONSTANT.local_path
nwp_file_handler = NwpFileHandler(ip, id, pw)
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
time_interval = ["2019-04-05 18", "2019-04-15 00"]
horizon_interval = [0, 12]
var_list = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]
nearest_type = 1
point = [(37.57142, 126.9658)]
current_time = datetime.datetime.now()

ftp_accessor = NwpFileHandler(ip, id, pw)
ftp_accessor.data_type_setting(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
ftp_accessor.set_file_names()
# ftp_accessor.check_total_size_of_files()
# ftp_accessor.save_file_from_ftp_server()
# df = ftp_accessor.extract_variable_values("training", var_list, 1, point)

with open("/home/jhpark/experiment_files/new.pkl", "rb") as f:
    df = pickle.load(f)

visualizer = Visualize()
visualizer.correlation_matrix(df, var_list)

# nwp_parsing_controller.extract_variable_values(ftp_accessor, data_type, fold_type, time_interval,
#                                                var_list, nearest_type, point,
#                                                output_file_name="experimental",
#                                                horizon_interval=horizon_interval)
#
# nwp_parsing_controller.remove_files(ftp_accessor, data_type, fold_type, time_interval, horizon_interval=horizon_interval)

# nwp_file_handler.data_type_setting(data_type, fold_type, time_interval, horizon_interval)
# print current_time-datetime.timedelta(days=11)
# print nwp_file_handler.find_nearest_nwp_prediction_file_in_local(current_time-datetime.timedelta(days=11), 10)

# ftp_accessor.save_target_file("RDAPS", "g120_v070_erea_pres_h060.2019041118.gb2", "/home/jhpark/experiment_sth")


##################################################################################################



if __name__ == "__main__":
    nwp_file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h000.2019041518.gb2")
    lat_grid, lon_grid = nwp_file[4].latlons()
    # point = (37.57142, 126.9658)
    #
    analyzer = NwpGridAnalyzer()
    analyzer.set_lat_lon_grid(lat_grid, lon_grid)
    # analyzer.plot_base_point(lat_point, lon_point, lat, lon)
    # analyzer.plot_nearest_point(analyzer.around_four_grid_point(point[0], point[1]), point[0], point[1])
    # analyzer.plot_nearest_n_point(analyzer.nearest_n_grid_point(20, point[0], point[1]), point[0], point[1])
    pass

