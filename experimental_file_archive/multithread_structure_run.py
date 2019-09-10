import filenameclass
import time

file_type = filenameclass.LdapsFile
time_interval = ["2019-08-10 00", "2019-08-12 12"]
fold_type = "unis"
location_points = [(36.149082, 127.175952)]
variables = ["NDNSW", "SWDIR", "SWDIF", "TDSWS", "NDNLW", "OULWT", "DLWS"]


container = filenameclass.FilesContainer(file_type, time_interval, fold_type,
                                         location_points, variables)
container.generate_base_files()
print(container.container.qsize())
# print(container.container.qsize())

analyzer = filenameclass.NwpGridAnalyzer()
# a = filenameclass.FilesContainer()

# for file in container.container:
#     print(file.name)

start_time = time.time()

master = filenameclass.DataOrganizer(analyzer, container)
master.data_collect(24)
print(master.total_df)

end_time = time.time()

print("progressed: ", end_time - start_time)

strided : start_time

