import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt

# dataset = pd.read_excel("/home/jhpark/experiment_files/510training.xlsx")
dataset = pd.read_excel("/home/jhpark/experiment_files/dailypredictioninput.xlsx")

df = np.array(dataset)

# print(dataset)
# print(df)

# training_X = df[:6000, :7]
# training_Y = df[:6000, 7]
#
prediction_X = df[:, :7]

print(prediction_X)
# real_Y = df[6000:, 7]
#
# print prediction_X
# print
# model = keras.Sequential()
# model.add(keras.layers.Dense(7, input_dim=7, activation="relu"))
# model.add(keras.layers.Dense(7, activation="relu"))
# model.add(keras.layers.Dense(7, activation="relu"))
# model.add(keras.layers.Dense(6, activation="relu"))
# model.add(keras.layers.Dense(5, activation="relu"))
# model.add(keras.layers.Dense(4, activation="relu"))
# model.add(keras.layers.Dense(4, activation="relu"))
# model.add(keras.layers.Dense(4, activation="relu"))
# model.add(keras.layers.Dense(1, activation="linear"))
#
# model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])
# model.fit(training_X, training_Y, epochs=200, batch_size=1000)
#
# model.save("521prediction.h5")

model = keras.models.load_model("521prediction.h5")
prediction = model.predict(prediction_X)
#
# print prediction
prediction = np.asarray([x[0] for x in prediction])
# np.savetxt("dailypredictionoutput.csv", prediction, delimiter=",")
#
# nape_list = np.abs(prediction - real_Y)/99
#
# print "------------------------------------------------------------"
# nmape = np.average(nape_list)
# print nmape
# print nape_list
# nmape = np.average(nape_list.nonzero())
# print nmape
#
# length = len(prediction)
# plt.plot(range(length), prediction)
# plt.plot(range(length), real_Y)
# # plt.plot(prediction, real_Y)
# plt.show()

