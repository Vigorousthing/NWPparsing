import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt

# dataset = pd.read_excel("/home/jhpark/experiment_files/510training.xlsx")
# dataset = pd.read_excel("/home/jhpark/experiment_files/all_variable_prediction_file.xlsx")
dataset = pd.read_excel("/home/jhpark/experiment_files/0409prediction_data.xlsx")

df = np.array(dataset)

# training_X = df[:7500, :7]
# training_Y = df[:7500, 7]
# # prediction_X = df[7500:, :7]
# real_Y = df[7500:, 7]

# training_X = df[:7500, :57]
# training_Y = df[:7500, 57]
# prediction_X = df[7500:, :57]
# real_Y = df[7500:, 57]

# training_X = df[:, :7]
# training_Y = df[:, 7]
prediction_X = df[:, :7]
real_Y = df[:, 7]

#
# print prediction_X
# model = keras.Sequential()
# model.add(keras.layers.Dense(57, input_dim=57, activation="relu"))
# model.add(keras.layers.Dense(57, activation="relu"))
# model.add(keras.layers.Dense(57, activation="relu"))
# model.add(keras.layers.Dense(27, activation="relu"))
# model.add(keras.layers.Dense(27, activation="relu"))
# model.add(keras.layers.Dense(14, activation="relu"))
# model.add(keras.layers.Dense(14, activation="relu"))
# model.add(keras.layers.Dense(7, activation="relu"))
# model.add(keras.layers.Dense(7, activation="relu"))
# model.add(keras.layers.Dense(1, activation="linear"))
#
# model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])
# model.fit(training_X, training_Y, epochs=200, batch_size=1000)
#
# model.save("520prediction.h5")


model = keras.models.load_model("521prediction.h5")

prediction = model.predict(prediction_X)

print prediction
prediction = np.asarray([x[0] for x in prediction])
np.savetxt("0409prediction.csv", prediction, delimiter=",")

nape_list = np.abs(prediction - real_Y)/99

print "------------------------------------------------------------"
nmape = np.average(nape_list)
print "nmape : ", nmape
# print nape_list
nmape = np.average(nape_list.nonzero())
print "nmape zero removed : ", nmape

length = len(prediction)
plt.plot(range(length), prediction)
plt.plot(range(length), real_Y)
# plt.plot(prediction, real_Y)
plt.show()

