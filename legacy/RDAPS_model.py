import pandas as pd
import numpy as np
import keras
import CONSTANT
import datetime
import matplotlib.pyplot as plt

location_dic = {1: "asos", 2: "office", 3: "plant"}
purpose_dict = {1: "training", 2: "prediction"}

location = 2
purpose = 2

# time = datetime.datetime.now()
# time_string = str(time.year)+str(time.month)+str(time.day)+str(time.hour)+str(time.second)

asos_dataset = pd.read_excel("/home/jhpark/experiment_files/training_ASOS_6m.xlsx")
office_dataset = pd.read_excel("/home/jhpark/experiment_files/training_office_6m.xlsx")
plant_dataset = pd.read_excel("/home/jhpark/experiment_files/training_plant_6m.xlsx")

asos_test_dataset = pd.read_excel(CONSTANT.prediction_input_output_path + "rdaps_asos_test_input.xlsx")
office_test_dataset = pd.read_excel(CONSTANT.prediction_input_output_path + "rdaps_office_test_input.xlsx")
plant_test_dataset = pd.read_excel(CONSTANT.prediction_input_output_path + "rdaps_plant_test_input.xlsx")

office_test_dataset = pd.read_excel(CONSTANT.prediction_input_output_path + "training_office_6m_no_real.xlsx")
office_test_dataset = pd.read_excel(CONSTANT.prediction_input_output_path + "forsubmit.xlsx")

if location == 1:
    df = np.array(asos_dataset)
    test_df = np.array(asos_test_dataset)
elif location == 2:
    df = np.array(office_dataset)
    test_df = np.array(office_test_dataset)
elif location == 3:
    df = np.array(plant_dataset)
    test_df = np.array(plant_test_dataset)

training_X = df[:, :7]
training_Y = df[:, 7]

prediction_X = test_df[:, :]
# real_Y = test_df[:, 7]

if purpose == 1:
    model = keras.Sequential()
    model.add(keras.layers.Dense(7, input_dim=7, activation="relu"))
    model.add(keras.layers.Dense(14, activation="relu"))
    model.add(keras.layers.Dense(21, activation="relu"))
    model.add(keras.layers.Dense(21, activation="relu"))
    model.add(keras.layers.Dense(21, activation="relu"))
    model.add(keras.layers.Dense(14, activation="relu"))
    model.add(keras.layers.Dense(14, activation="relu"))
    model.add(keras.layers.Dense(7, activation="relu"))
    model.add(keras.layers.Dense(7, activation="relu"))
    model.add(keras.layers.Dense(1, activation="linear"))

    model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])
    model.fit(training_X, training_Y, epochs=50, batch_size=1000)

    model.save(CONSTANT.model_path+"rdaps"+location_dic[location]+".h5")

elif purpose == 2:
    model = keras.models.load_model(CONSTANT.model_path+"rdaps"+location_dic[location]+".h5")
    prediction = model.predict(prediction_X)
    prediction = np.asarray([x[0] for x in prediction])
    # np.savetxt(CONSTANT.prediction_input_output_path+purpose_dict[purpose]+location_dic[location]+".csv", prediction, delimiter=",")
    np.savetxt("fufu.csv", prediction, delimiter=",")

# nape_list = np.abs(prediction - real_Y)/99
#
# print("------------------------------------------------------------")
# nmape = np.average(nape_list)
# print("nmape : ", nmape)
# # print nape_list
# nmape = np.average(nape_list.nonzero())
# print("nmape zero removed : ", nmape)
#
# length = len(prediction)
# plt.plot(range(length), prediction)
# plt.plot(range(length), real_Y)
# # plt.plot(prediction, real_Y)
# plt.show()

