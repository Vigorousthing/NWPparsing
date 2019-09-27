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

start_time = time.time()

file_type = LdapsFile
current_time = "2019-09-10 10"
fold_type = "unis"
location_points = get_sitelist(MongodbConnector("sites", "sitesList").
                               find_latest())["Coordinates"].get_values().tolist()
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC", "TMP", "SPFH",
             "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]
for_vpp_real_query = ""

mongo_connector = MongodbConnector("sites", "production")
ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id, CONSTANT.ftp_pw)
analyzer = NwpGridAnalyzer()
visualizer = Visualizer()
container = FilesContainer(file_type, fold_type, location_points, variables)

vpp_real_result = mongo_connector.aggregate(for_vpp_real_query)
prediction_result = create_current_prediction(container, ftp_accessor, analyzer, current_time, "0924newmodel.h5")


# print(result[["CRTN_TM", "new_horizon", "horizon", "FCST_TM"]])

end_time = time.time()
print("passed: ", end_time - start_time)

