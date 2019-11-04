from data_accessors.MongoDbConnector import *
import time
from nwp_object.NwpFile import *
from controllers.prediction_maker import RealTimePredictionMakerForAllVpp

fold_type = "unis"
plant_id_list = "all"
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list, get_site_info_df())

ldaps_variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]
rdaps_variables = ["NDNSW", "XGWSS", "YGWSS", "LLRIB", "HFSFC", "TMOFS",
                   "SHFO", "SUBS", "TMP", "TMIN", "TMAX", "UCAPE", "UPCIN",
                   "LCDC", "MCDC", "HCDC", "TCAR", "TCAM", "TMP-SFC", "PRES"]

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
                                                  ldaps_variables,
                                                  rdaps_variables,
                                                  ldaps_model_name,
                                                  rdaps_model_name)
    ldaps_df, rdaps_df = controller.create_realtime_prediction()

    prediction_df = unified_df(
        ldaps_df, rdaps_df, ldaps_variables, rdaps_variables)
    nwp_df = column_subtract(ldaps_df, ["GEN_NAME", "capacity", "FCST_QGEN"])

    prediction_df.to_excel(CONSTANT.data_file_path + "test_1104.xlsx")
    nwp_df.to_excel(CONSTANT.data_file_path + "test_nwp_1104.xlsx")

    end_time = time.time()
    print("total time progressed: ", (end_time - start_time))
