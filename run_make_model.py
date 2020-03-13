# maker1 = VppTraining(LdapsFile, "unis",
#                     [2019102400, 2019102406], ["P31S2105", "P31S51157"],
#                     ["NDNSW"])
# maker2 = JenonTraining(RdapsFile, "unis", [2019080100, 2019093023],
#                        ["NDNSW", "XGWSS", "YGWSS", "LLRIB", "HFSFC",
#                         "TMOFS", "SHFO", "SUBS", "TMP", "TMIN",
#                         "TMAX", "UCAPE", "UPCIN", "LCDC", "MCDC",
#                         "HCDC", "TCAR", "TCAM", "TMP-SFC", "PRES"])

# maker1.create_nwp_checkpoint("ldaps_checkpoint")
# maker2.create_nwp_checkpoint("rdaps_checkpoint09")

# df = maker1.create_training_data_ldaps("ldaps_checkpoint")
# lists = maker2.create_training_data_rdaps("rdaps_checkpoint0809")

# modelob = RdapsModelObject(lists[0], lists[1])
# modelob.create_new_model("rdaps.h5", 30)


from controllers.model_makers import *
import numpy as np
import pandas as pd


training_input_file = pd.read_excel(
    CONSTANT.data_file_path + "svg_trrd_6to12.xlsx")
# training_input_file = np.array(training_input_file)
training_input_file = training_input_file[training_input_file.location_num
                                          == 0]
# print(training_input_file.CRTN_TM)

# training_input_file = training_input_file[(training_input_file.CRTN_TM.dt.hour
#                                           == 15) |
#                                           (training_input_file.CRTN_TM.dt.hour
#                                           == 9)]

print(training_input_file)

model_input_var = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]
# model_input_var = ["NDNSW", "UGRD", "VGRD", "TMP", "SPFH", "RH", "DPT"]



model_name = "nonje_1016model.h5"
# model_name = "20200310svr.pkl"
# model_name = "20200310ann.h5"
# model_name = "20200311xgb"

l_modelob = LdapsModelObject(training_input_file, model_input_var)
l_modelob.split_training_data_for_eval(0.8)
# l_modelob.create_svr_model("20200302svr0th.pkl")
# l_modelob.create_ann_model("20200306ann0th0.h5", 5)
# l_modelob.create_svr_model("20200306svr0th0.pkl")

# l_modelob.create_ann_model("20200310ann.h5", 25)
# l_modelob.create_svr_model("20200310svr.pkl")
# l_modelob.create_xgb_model(model_name)

l_modelob.set_exist_model(model_name)
df = l_modelob.eval_model()
df.to_excel(CONSTANT.data_file_path + "20200312" + model_name + "result.xlsx")
