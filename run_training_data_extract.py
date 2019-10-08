from controller import *
from nwp_object.NwpFile import *

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = LdapsFile
time_interval = [2019070100, 2019073123]
fold_type = "unis"
# location_points = [(36.149082, 127.175952)]
# location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]
plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530",
                 "P41S21482"]
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list)
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        time_interval, plant_location_list, variables)
controller.create_training_df("7mvpptraining")
end_time = time.time()
print("total time progressed: ", (end_time - start_time)/60)
