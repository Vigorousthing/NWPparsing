from controller import *
from nwp_object.NwpFile import *
import datetime
import pymongo

file_type = LdapsFile
now = datetime.datetime.now()
fold_type = "unis"
plant_id_list = "all"
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list, get_site_info_df())

variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        now, plant_location_list, variables)
df = controller.create_realtime_prediction("nonje_1016model.h5")
end_time = time.time()

prediction_df = df.drop(columns=variables)
nwp_df = df.drop(columns=["GEN_NAME", "capacity", "FCST_QGEN"])

connection = pymongo.MongoClient("mongodb://datanode4:27017")

sites_db = connection.sites
kma_db = connection.kma

fcst_production_keti = sites_db.fcst_production_keti
keti_nwp = kma_db.keti_nwp

fcst_production_keti.insert_many(prediction_df.to_dict("records"))
keti_nwp.insert_many(nwp_df.to_dict("records"))

connection.close()

print("total time progressed: ", (end_time - start_time))


