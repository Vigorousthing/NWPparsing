import pandas as pd
import keras
import numpy as np
import CONSTANT


def model_create(model_name, base_filename, training_rate, site, column_idx):
    df, t_idx = base_setting(base_filename, training_rate, site)

    training_X = df[:t_idx, column_idx:-1]
    training_Y = df[:t_idx, -1]

    model = modelling(training_X, training_Y)
    model.save("data_file/model_files/"+model_name)


def model_evaluation(model_name, base_filename, training_rate, site,
                     column_idx, same_with_training=False):
    df, t_idx = base_setting(base_filename, training_rate, site)

    if same_with_training == False:
        prediction_X = df[t_idx:, column_idx:-1]
        real_Y = df[t_idx:, -1]
    else:
        prediction_X = df[:t_idx, column_idx:-1]
        real_Y = df[:t_idx, -1]

    model = keras.models.load_model("data_file/model_files/"+model_name)
    prediction = model.predict(prediction_X)

    prediction = np.asarray([x[0] for x in prediction])

    result = evaluation(prediction, real_Y)
    print(result)
    # plt.plot(prediction)
    # plt.plot(real_Y)
    # plt.show()


def modelling(training_input, training_real):
    model = keras.Sequential()
    model.add(keras.layers.Dense(6, input_dim=6, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
    model.add(keras.layers.Dense(10, activation="relu"))
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


def base_setting(base_filename, training_rate, site):
    base_df = pd.read_excel(CONSTANT.exp_file_path + base_filename)
    if site == None:
        pass
    else:
        base_df = base_df[base_df.site == site]

    df = np.array(base_df)
    df_len = df.shape[0]
    training_index = int(df_len*training_rate)
    return df, training_index


training_rate = 0.8
site = None
column_idx = 0
base_filename = "nonje_with_real_base_abb.xlsx"
epoch = 50


if __name__ == "__main__":
    model_name = "1002abbmodel.h5"
    # base_file_create()
    model_create(model_name, base_filename, training_rate, site, column_idx)
    model_evaluation(model_name, base_filename, training_rate, site,
                     column_idx, same_with_training=False)
