from controller import *
from nwp_object.NwpFile import *
import datetime

file_type = LdapsFile
now = datetime.datetime.now()
fold_type = "unis"
plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530", "P41S21482"]
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list)
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        now, plant_location_list, variables)
df = controller.create_realtime_prediction("vppmodel.h5")
print(df)
end_time = time.time()
print("total time progressed: ", (end_time - start_time)/60)
