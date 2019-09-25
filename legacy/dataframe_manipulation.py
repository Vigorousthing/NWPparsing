import pandas as pd
import keras
import numpy as np

basic_path = "/home/jhpark/experiment_files/"
irr_file = "seoul_asos_irr_real.xlsx"
nwp_file = "nwp_prediction.xlsx"

irr_path = basic_path + irr_file
nwp_path = basic_path + nwp_file

irr_df = pd.read_excel(irr_path)
nwp_df = pd.read_excel(nwp_path)

nwp_df['CRTN_TM'] = pd.to_datetime(nwp_df['CRTN_TM'])
nwp_df['FCST_TM'] = pd.to_datetime(nwp_df['FCST_TM'])
# irr_df = irr_df.rename(columns={"CRTN_TM": "FCST_TM"})


# print type(irr_df), type(nwp_df)
# print irr_df.dtypes, nwp_df.dtypes

merged = pd.merge(nwp_df, irr_df, how="inner", on="FCST_TM")

merged.to_excel("merged_file.xlsx")
# print type(merged["IRR-W"])

Y = np.array(merged)[:, -1]
X = np.array(merged)[:, 3:-1]


# print pd.DataFrame(Y)
# print pd.DataFrame(X)
# print merged
#
model = keras.models.Sequential()
model.add(keras.layers.Dense(20, input_shape=(7,), activation="relu"))
model.add(keras.layers.Dense(20, activation="relu"))
model.add(keras.layers.Dense(15, activation="relu"))
model.add(keras.layers.Dense(15, activation="relu"))
model.add(keras.layers.Dense(10, activation="relu"))
model.add(keras.layers.Dense(5, activation="relu"))
model.add(keras.layers.Dense(1, activation="linear"))

model.compile(loss="mean_squared_error", optimizer="adam")
model.fit(X, Y, epochs=5, validation_split=0.2)

model.save("irr_prediction_model.h5")

# scores = model.evaluate(X, Y)