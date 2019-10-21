from data_accessors.MongoDbConnector import *
import time
from nwp_object.NwpFile import *
from controllers.prediction_maker import RealTimePredictionMaker

file_type = LdapsFile
fold_type = "unis"
plant_id_list = "all"
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list, get_site_info_df())

variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]

start_time = time.time()
controller = RealTimePredictionMaker(file_type, fold_type,
                                     plant_location_list, variables,
                                     "nonje_1016model.h5")
df = controller.create_realtime_prediction()
end_time = time.time()

print(df.dtypes)
df.to_excel(CONSTANT.data_file_path + "after_refactor_df.xlsx")

# prediction_df = df.drop(columns=variables)
# nwp_df = df.drop(columns=["GEN_NAME", "capacity", "FCST_QGEN"])

print("total time progressed: ", (end_time - start_time))


