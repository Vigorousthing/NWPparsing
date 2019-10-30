from util.Visualizer import Visualizer
import pandas as pd
import CONSTANT

# column = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
#              "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC", "real"]
# df = pd.read_excel(CONSTANT.data_file_path + "nonje_with_real_base.xlsx")
# df = df.drop(columns=["Coordinates", "CRTN_TM", "FCST_TM", "horizon", "site"])
# visualizer = Visualizer()
# visualizer.correlation_matrix(df, column)


# after = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC", "real"]

# df = pd.read_excel(CONSTANT.data_file_path + "jeju_asos_data.xlsx")
# visualizer = Visualizer()
# visualizer.correlation_matrix(df, ["real", "insolation", "intemp", "outtemp",
#                                    "total_cloud", "ws", "wd", "hd", "hPa",
#                                    "dtp", "ap"])

# df2 = pd.read_excel(CONSTANT.data_file_path + "nonje_visualize.xlsx")
# visualizer = Visualizer()
# visualizer.correlation_matrix(df2, ["real", "NDNSW", "SWDIR", "SWDIF", "TDSWS",
#                                    "UGRD", "VGRD", "HFSFC", "TMP", "SPFH",
#                                    "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"])

df = pd.read_excel(CONSTANT.data_file_path + "jeju_asos_data.xlsx")
visualizer = Visualizer()
visualizer.correlation_matrix(df, ["real", "insolation", "intemp", "outtemp",
                                   "total_cloud", "ws", "wd", "hd", "hPa",
                                   "dtp", "ap"])
