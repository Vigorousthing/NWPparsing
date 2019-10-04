from util.Visualizer import Visualizer
import pandas as pd
import numpy as np
import CONSTANT

column = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC", "real"]

df = pd.read_excel(CONSTANT.exp_file_path + "nonje_with_real_base.xlsx")
df = df.drop(columns=["Coordinates", "CRTN_TM", "FCST_TM", "horizon", "site"])

visualizer = Visualizer()
visualizer.correlation_matrix(df, column)


after = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC", "real"]

