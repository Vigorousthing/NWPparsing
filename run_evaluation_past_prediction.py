from nwp_object.NwpFile import LdapsFile
from controller import *

'''
case code
evaluation with vpp site : 1
evaluation with jenon site : 2
'''


file_type = LdapsFile
time_interval = [2019060100, 2019060113]
fold_type = "unis"
# location_points = get_sitelist(
#     MongodbConnector("sites", "sitesList").
#     find_latest())["Coordinates"].get_values().tolist()
plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530", "P41S21482"]
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]
# variable collection used as models input should be documented
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

controller = Controller(file_type, fold_type, time_interval, location_points,
                        variables)

prediction_df = controller.create_interval_prediction("hourly", "vppmodel.h5")
real_df = controller.create_real_vpp(time_interval, plant_id_list)

df = controller.evaluation_model("vppmodel.h5")
print(df)
