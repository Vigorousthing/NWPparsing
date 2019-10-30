import time
from controllers.training_maker import VppTraining
from nwp_object.NwpFile import *

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = LdapsFile
time_interval = [2019060100, 2019060223]
fold_type = "unis"
plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530",
                 "P41S21482"]

variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

start_time = time.time()
controller = VppTraining(file_type, fold_type, time_interval, plant_id_list,
                         variables)

controller.create_training_df("6m2dtest")
end_time = time.time()
print("total time progressed: {} minutes".format((end_time - start_time)/60))
