import time
import CONSTANT
from nwp_object.NwpFile import LdapsFile
from nwp_object.FilesContainer import FilesContainer
from data_extract.DataOrganizer import DataOrganizer
from data_accessors.FtpAccessor import FtpAccessor
from util.NwpGridAnalyzer import NwpGridAnalyzer
from util.Visualizer import Visualizer
from util.QueueJobProgressIndicator import QueueJobProgressIndicator


# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = LdapsFile

time_interval_list = [
    # ["2019-06-01 00", "2019-06-10 23"],
    # ["2019-06-11 00", "2019-06-20 23"],
    # ["2019-06-21 00", "2019-06-30 23"],
    # ["2019-07-01 00", "2019-07-10 23"],
    # ["2019-07-21 00", "2019-07-25 23"],
    # ["2019-07-26 00", "2019-07-31 23"],
    # ["2019-08-01 00", "2019-08-10 23"],
    # ["2019-08-11 00", "2019-08-20 23"],
    # ["2019-08-21 00", "2019-08-26 23"],
    # ["2019-08-27 00", "2019-08-31 23"],
]

time_interval_list = [
    ["2019-06-01 00", "2019-06-10 23"],
    # ["2019-07-11 00", "2019-07-12 04"],
    # ["2019-07-14 00", "2019-07-15 04"],
]

fold_type = "unis"
# location_points = [(36.149082, 127.175952)]
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "UGRD", "VGRD", "HFSFC", "TMP", "SPFH", "RH", "DPT", "TCAR", "TCAM",
             "TMP-SFC"]

ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id, CONSTANT.ftp_pw)
analyzer = NwpGridAnalyzer()
visualizer = Visualizer()

# time_interval = ["2019-06-01 00", "2019-06-01 06"]
# container = filenameclass.FilesContainer(file_type, time_interval, fold_type,
#                                          location_points, variables)
# container.generate_base_files()
# print(container.container.qsize())
# analyzer = filenameclass.NwpGridAnalyzer()
#
start_time = time.time()
# master = filenameclass.DataOrganizer(analyzer, container)
# master.data_collect(10)
# print(master.total_df)



def controll(time_interval_list, ftp_accessor, analyzer, file_type):

    df = None
    for i, time_interval in enumerate(time_interval_list):

        container = FilesContainer(file_type, fold_type, location_points, variables)

        container.generate_base_files(time_interval)
        filename_list = container.filename_list
        if not ftp_accessor.check_connection():
            ftp_accessor.reconnect()
        ftp_accessor.download_files(filename_list, file_type.nwp_type)

        queuejobchecker = QueueJobProgressIndicator(container.container)
        queuejobchecker.start()

        start = time.time()
        master = DataOrganizer(analyzer, container)
        temp_df = master.data_collect(10)
        temp_df.to_excel("/home/jhpark/experiment_files/" + "temp_file_" + str(i) + ".xlsx")

        if i == 0:
            df = temp_df
        else:
            df = df.append(temp_df)

        end = time.time()
        # ftp_accessor.remove_from_local_pc(filename_list)
        # remove_process
        print("passed in {}th iteration : ".format(i), end - start)
        queuejobchecker.terminate()

    df.to_excel("/home/jhpark/experiment_files/" + "errortest6m" + ".xlsx")


# controll(time_interval_list, ftp_accessor, analyzer, file_type)
# end_time = time.time()
# print("progressed: ", end_time - start_time)

prediction_container = FilesContainer(file_type, fold_type, location_points, variables)
prediction_container.generate_base_prediction_files("2019-09-24 20")
