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
from controller import *

file_type = LdapsFile
current_time = 2019091010
time_interval = [2019060100, 2019061023]
fold_type = "unis"
location_points = get_sitelist(
    MongodbConnector("sites", "sitesList").
    find_latest())["Coordinates"].get_values().tolist()

# variable collection used as models input should be documented
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC",
             "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM", "TMP-SFC"]

controller = Controller(file_type, fold_type, current_time, location_points,
                        variables)
df = controller.create_current_predcition("0930newmodel.h5")

print(df)