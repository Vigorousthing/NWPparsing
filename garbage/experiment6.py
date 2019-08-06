import keras
import df_load

model = keras.models.load_model("irr_prediction_model.h5")
# y = model.predict()


import datetime

print datetime.datetime.strptime("2019-09-20", "%Y-%m-%d")
print datetime.datetime.now() - datetime.datetime.strptime("2019-09-20", "%Y-%m-%d")


print abs((datetime.datetime.now() - datetime.datetime.strptime("2019-09-20", "%Y-%m-%d")).days)

import pickle

with open("/home/jhpark/experiment_files/training2019-03-052019-05-01.pkl", "rb") as df:
    df = pickle.load(df)
    print df
    print type(df)
    print df.dtypes

df = df_load.real_df_load(df_load.config_info, df_load.target_plants, df_load.after_this_time)

df = df.toPandas()

df.to_csv("/home/jhpark/experiment_files/pddf_real_vpp_data.csv", header=True)

print df
print type(df)
print df.dtypes

