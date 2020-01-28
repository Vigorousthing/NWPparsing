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
    CONSTANT.data_file_path + "20200128ldapssvrtestinputoutput.xlsx")
# training_input_file = np.array(training_input_file)

free = np.array(training_input_file[["NDNSW", "HFSFC", "TMP", "RH",
                                     "TMP-SFC"]])
dpnt = np.array(training_input_file["real"])

l_modelob = LdapsModelObject(free, dpnt)
l_modelob.split_training_data_for_eval(0.1)
l_modelob.create_svr_model("20200128svr.pkl")
