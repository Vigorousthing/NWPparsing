from nwp_object.NwpFile import *
from util.query_maker import *
from controller import *
import CONSTANT

time_interval = [2019060100, 2019083123]
plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530", "P41S21482"]
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list)

mongo_connector = MongodbConnector("sites", "production")
mongo_connector2 = MongodbConnector("sites", "sitesList")
query = vpp_production_query(time_interval, match_plant_subquery(plant_id_list))

real_df = mongo_connector.aggregate(query)
site_info_df = get_sitelist(mongo_connector2.find_latest())

real_df = real_df.drop(columns=["_id"])
site_info_df = site_info_df.rename(columns={"site": "COMPX_ID"})
merged = pd.merge(real_df, site_info_df, how="left", on=["COMPX_ID"])
training_df = pd.read_excel(CONSTANT.path)

# print(merged)

file_type = LdapsFile
fold_type = "unis"
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

controller = Controller(file_type, fold_type,
                        time_interval, plant_location_list, variables)
