from nwp_object.NwpFile import *
from model_create_jenon import *
from util.query_maker import *
from controller import *
import CONSTANT


def create_input():
    time_interval = [2019060100, 2019083123]
    plant_id_list = ["P31S2105", "P31S51157", "P61S2102", "P61S31530", "P41S21482"]
    location_num_table = pd.DataFrame(
        list(zip(plant_id_list, [i for i in range(len(plant_id_list))])),
        columns=["COMPX_ID", "location_num"])

    mongo_connector = MongodbConnector("sites", "production")
    mongo_connector2 = MongodbConnector("sites", "sitesList")
    query = vpp_production_query(time_interval,
                                 match_plant_subquery(plant_id_list))

    real_df = mongo_connector.aggregate(query)
    site_info_df = get_sitelist(mongo_connector2.find_latest())

    real_df = real_df.drop(columns=["_id"])
    site_info_df = site_info_df.rename(columns={"site": "COMPX_ID"})
    site_info_df = pd.merge(site_info_df, location_num_table, how="left",
                            on=["COMPX_ID"])

    merged = pd.merge(real_df, site_info_df, how="left", on=["COMPX_ID"])
    merged = merged.rename(columns={"CRTN_TM": "FCST_TM"})
    merged = merged.rename(columns={"lng": "lon"})
    training_df = pd.read_excel(CONSTANT.data_file_path +
                                "vpp_training_data.xlsx")

    # type conversion
    merged["lat"] = pd.to_numeric(merged["lat"])
    merged["lon"] = pd.to_numeric(merged["lon"])

    # merged.to_excel(CONSTANT.data_file_path + "{}.xlsx".format("mergedd"))

    # final input
    ready_to_fit = pd.merge(training_df, merged, how="left",
                            on=["location_num", "FCST_TM"])
    return ready_to_fit


training_rate = 0.8
site = None
column_idx = 0
base_filename = "ready_to_fit.xlsx"
epoch = 50
model_name = "vppmodel.h5"


if __name__ == "__main__":
    # model_create(model_name, base_filename, training_rate, site, column_idx)
    model_evaluation(model_name, base_filename, training_rate, site,
                     column_idx, same_with_training=False)
