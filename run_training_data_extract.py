from controller import *
from nwp_object.NwpFile import *

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = LdapsFile
time_interval = [2019080100, 2019083123]

fold_type = "unis"
# location_points = [(36.149082, 127.175952)]
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        time_interval, location_points, variables)
controller.create_training_df("6mvpptraining")
end_time = time.time()
print("total time progressed: ", (end_time - start_time)/60)
