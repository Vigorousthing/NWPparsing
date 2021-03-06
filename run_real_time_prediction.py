from data_accessors.MongoDbConnector import *
import time
from nwp_object.NwpFile import *
from controllers.prediction_maker import RealTimePredictionMakerForAllVpp

release = False

fold_type = "unis"
plant_id_list = "all"
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list, get_site_info_df())

ldaps_model_name = "nonje_1016model.h5"
rdaps_model_name = "rdaps.h5"


def column_subtract(df, col_list):
    result = df.drop(columns=col_list)
    result.reset_index(drop=True, inplace=True)
    return result


def unified_df(ldaps, rdaps, l_var, r_var):
    ldaps = ldaps.drop(columns=l_var)
    rdaps = rdaps.drop(columns=r_var)
    result = ldaps.append(rdaps, sort=False)
    result = result.sort_values(by=["COMPX_ID", "LEAD_HR"],
                                ascending=True)
    result.reset_index(drop=True, inplace=True)
    return result


if __name__ == '__main__':
    start_time = time.time()
    controller = RealTimePredictionMakerForAllVpp(fold_type,
                                                  plant_location_list,
                                                  ldaps_model_name,
                                                  rdaps_model_name)
    ldaps_df, rdaps_df = controller.create_prediction(remove=release)
    prediction_df = unified_df(ldaps_df, rdaps_df,
                               controller.ldaps_variables,
                               controller.rdaps_variables)

    if release is True:
        nwp_df = column_subtract(ldaps_df,
                                 ["GEN_NAME", "capacity", "FCST_QGEN"])

        connection = pymongo.MongoClient("mongodb://datanode4:27017")
        sites_db = connection.sites
        kma_db = connection.kma

        fcst_production_keti = sites_db.fcst_production_keti
        keti_nwp = kma_db.keti_nwp

        # unified df
        fcst_production_keti.insert_many(prediction_df.to_dict("records"))

        # nwp data db. ldaps - variables
        keti_nwp.insert_many(nwp_df.to_dict("records"))

        end_time = time.time()
        print("total time progressed: ", (end_time - start_time))
    else:
        prediction_df.to_excel(CONSTANT.data_file_path +
                               "prediction_df_test.xlsx")
        print(prediction_df)
