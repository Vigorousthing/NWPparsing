import filenameclass
import time
import CONSTANT

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = filenameclass.LdapsFile

time_interval_list = [
    ["2019-06-01 00", "2019-06-10 23"],
    ["2019-06-11 00", "2019-06-20 23"],
    ["2019-06-21 00", "2019-06-30 23"],
    ["2019-07-01 00", "2019-07-10 23"],
    ["2019-07-11 00", "2019-07-20 23"],
    ["2019-07-21 00", "2019-07-31 23"],
    ["2019-08-01 00", "2019-08-10 23"],
    ["2019-08-11 00", "2019-08-20 23"],
    ["2019-08-21 00", "2019-08-31 23"],
]

time_interval_list = [
    ["2019-06-01 00", "2019-06-01 04"],
    ["2019-07-11 00", "2019-07-11 04"],
]

fold_type = "unis"
# location_points = [(36.149082, 127.175952)]
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]

ftp_accessor = filenameclass.FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id, CONSTANT.ftp_pw)
analyzer = filenameclass.NwpGridAnalyzer()

# time_interval = ["2019-06-01 00", "2019-06-01 06"]
# container = filenameclass.FilesContainer(file_type, time_interval, fold_type,
#                                          location_points, variables)
# container.generate_base_files()
# print(container.container.qsize())
# analyzer = filenameclass.NwpGridAnalyzer()
#
# start_time = time.time()
# master = filenameclass.DataOrganizer(analyzer, container)
# master.data_collect(10)
# print(master.total_df)
# end_time = time.time()
# print("progressed: ", end_time - start_time)

def controll(time_interval_list, ftp_accessor, analyzer, file_type):
    df = None
    for i, time_interval in enumerate(time_interval_list):
        container = filenameclass.FilesContainer(file_type, time_interval, fold_type,
                                                 location_points, variables)
        container.generate_base_files()
        filename_list = container.filename_list
        ftp_accessor.download_files(filename_list, file_type.nwp_type)

        master = filenameclass.DataOrganizer(analyzer, container)
        temp_df = master.data_collect(6)
        if i == 0:
            df = temp_df
        else:
            df = df.append(temp_df)

        ftp_accessor.remove_from_local_pc(filename_list)
        # remove_process

    return df

df = controll(time_interval_list, ftp_accessor, analyzer, file_type)
