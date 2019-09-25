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
current_time = "2019-09-10 10"
fold_type = "unis"
location_points = get_sitelist(MongodbConnector("sites", "sitesList").
                               find_latest())["Coordinates"].get_values().tolist()
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]

variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC", "TMP", "SPFH",
             "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]


ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id, CONSTANT.ftp_pw)
analyzer = NwpGridAnalyzer()
visualizer = Visualizer()
container = FilesContainer(file_type, fold_type, location_points, variables)
# master = DataOrganizer(analyzer, container)

result = create_prediction(container, ftp_accessor, analyzer, current_time, "0924newmodel.h5")
result = result.drop(columns=["CRTN_TM"])

print(result)

