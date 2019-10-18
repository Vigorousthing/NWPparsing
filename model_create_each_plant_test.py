import keras
import numpy as np
import pandas as pd
import CONSTANT


def base_setting(base_file, training_rate, site):
    df = base_file[base_file.location_num == site]
    df = df.drop(columns=["location_num"])

    df = np.array(df)
    df_len = df.shape[0]
    training_index = int(df_len*training_rate)
    return df, training_index


def model_create(model_name, base_file, training_rate, site):
    df, t_idx = base_setting(base_file, training_rate, site)

    training_X = df[:t_idx, :-1]
    training_Y = df[:t_idx, -1]

    model = modelling(training_X, training_Y)
    model.save("data_file/model_files/"+model_name)


def model_evaluation(model_name, base_file, training_rate, site,
                     same_with_training=False):
    df, t_idx = base_setting(base_file, training_rate, site)

    if same_with_training == False:
        prediction_X = df[t_idx:, :-1]
        real_Y = df[t_idx:, -1]
    else:
        prediction_X = df[:t_idx, :-1]
        real_Y = df[:t_idx, -1]

    model = keras.models.load_model("data_file/model_files/"+model_name)
    prediction = model.predict(prediction_X)

    prediction = np.asarray([x[0] for x in prediction])

    result = evaluation(prediction, real_Y)
    print(result)


def modelling(training_input, training_real):
    model = keras.Sequential()
    model.add(keras.layers.Dense(5, input_dim=5, activation="relu"))
    model.add(keras.layers.Dense(5, activation="relu"))
    model.add(keras.layers.Dense(5, activation="relu"))
    model.add(keras.layers.Dense(5, activation="relu"))
    model.add(keras.layers.Dense(5, activation="relu"))
    model.add(keras.layers.Dense(1, activation="relu"))
    model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

    model.fit(training_input, training_real, epochs=epoch)
    return model


def evaluation(prediction, real):
    nape_list = np.abs(prediction - real)/99
    nape_list = list(nape_list)
    num = 0
    for i in nape_list:
        num += i
    nmape = num/len(nape_list)
    return nmape


training_rate = 0.8

plant_num = 2
base_file = pd.read_excel(CONSTANT.data_file_path + "vpp_each_base.xlsx")
epoch = 15
model_name = "vpp{}_1017.h5".format(plant_num)
# model_name = "vpp2_1017.h5"

# each = True
each = False
eval = True
# eval = False


if __name__ == "__main__":
    if each is False:
        for i in range(5):
            model_name = "vpp{}_1017.h5".format(i)
            if eval is False:
                model_create(model_name, base_file, training_rate, i)
                model_evaluation(model_name, base_file, training_rate, i,
                                 same_with_training=False)
            elif eval is True:
                model_evaluation(model_name, base_file, training_rate, i,
                                 same_with_training=False)
    elif each is True:
        model_name = "vpp{}_1017.h5".format(plant_num)
        if eval is False:
            model_create(model_name, base_file, training_rate, plant_num)
            model_evaluation(model_name, base_file, training_rate, plant_num,
                             same_with_training=False)
        elif eval is True:
            model_evaluation(model_name, base_file, training_rate, plant_num,
                             same_with_training=False)

