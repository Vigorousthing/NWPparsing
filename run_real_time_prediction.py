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
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        now, plant_location_list, variables)
df = controller.create_realtime_prediction("vppmodel.h5")
end_time = time.time()

print(df)

connection = pymongo.MongoClient("mongodb://datanode4:27017")
sites_db = connection.sites
fcst_production_keti = sites_db.fcst_production_keti
fcst_production_keti.insert_many(df.to_dict("records"))

print("total time progressed: ", (end_time - start_time))


