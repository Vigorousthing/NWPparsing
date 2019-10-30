from controller import *
from nwp_object.NwpFile import *

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83

file_type = RdapsFile
time_interval = [2019080100, 2019080323]
fold_type = "unis"
location_points = [(33.2875, 126.648611), (36.149019, 127.176031)]

variables = ["NDNSW", "XGWSS", "YGWSS", "LLRIB", "HFSFC",
             "TMOFS", "SHFO", "SUBS", "TMP", "TMIN",
             "TMAX", "UCAPE", "UPCIN", "LCDC", "MCDC",
             "HCDC", "TCAR", "TCAM", "TMP-SFC",
             "PRES"]

start_time = time.time()
controller = Controller(file_type, fold_type,
                        time_interval, location_points, variables)
df = controller.create_training_df("rdaps_exp")
end_time = time.time()
print("total time progressed: ", (end_time - start_time)/60)

print(df)


