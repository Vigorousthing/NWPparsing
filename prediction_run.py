import time
import CONSTANT
from nwp_object.NwpFile import LdapsFile
from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from data_accessors.MongoDbConnector import *
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.QueueJobProgressIndicator import QueueJobProgressIndicator
from controller_functions import *

file_type = LdapsFile
current_time = 2019091010
time_interval = [2019060100, 2019061023]
fold_type = "unis"
location_points = get_sitelist(MongodbConnector("sites", "sitesList").
                               find_latest())["Coordinates"].get_values().tolist()
# variable collection used as models input should be documented
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC", "TMP", "SPFH",
             "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

controller = Controller(file_type, fold_type, current_time, location_points,
                        variables)
df = controller.create_current_predcition("0930newmodel.h5")

print(df)
# df.to_excel("/home/jhpark/experiment_files/prediction_exp.xlsx")
# vpp_real_result = mongo_connector.aggregate(vpp_production_query(time_interval))
# prediction_result = create_current_prediction(container, ftp_accessor, analyzer,
#                                               current_time, "0924newmodel.h5")

