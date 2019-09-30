import pandas as pd
from data_accessors.DbConnector import DbConnector
import keras
import numpy as np
import matplotlib.pyplot as plt

# jeju(kyungsu) : (33.2875, 126.648611), capacity : 99
# nonsan(yj3-gayagok/yj2-yujin) : (36.149019, 127.176031), capacity : 99.83


def base_file_create():
    sql = "select tbl_inverter_min.recvdate - INTERVAL 10 MINUTE + INTERVAL 1 HOUR, sum(tbl_inverter_min.KWD), " \
          "avg(tbl_kma_min.intemp), avg(tbl_kma_min.outtemp), avg(tbl_kma_min.insolS) from tbl_inverter_min INNER JOIN " \
          "tbl_kma_min ON tbl_inverter_min.recvdate = tbl_kma_min.recvdate WHERE tbl_inverter_min.recvdate BETWEEN " \
          "'2019-04-30' AND '2019-09-05' GROUP BY MONTH(tbl_inverter_min.recvdate), DAY(tbl_inverter_min.recvdate), " \
          "HOUR(tbl_inverter_min.recvdate - INTERVAL 10 MINUTE) ORDER BY tbl_inverter_min.recvdate"

    nwp_df = pd.read_excel("/home/jhpark/data_files/jejunonsan_training_nwp.xlsx")

    jeju_connector = DbConnector("jeju")
    nonsan_connector = DbConnector("nonsan")

    jeju_real_df = pd.DataFrame(list(jeju_connector.query(sql)), columns=["FCST_TM",
                                                        "sum(tbl_inverter_min.KWD)", "avg(tbl_kma_min.intemp)",
                                                        "avg(tbl_kma_min.outtemp)", "avg(tbl_kma_min.insolS)"])
    jeju_real_df.insert(0, "Coordinates", [str((33.2875, 126.648611)) for i in range(jeju_real_df.shape[0])], True)
    nonsan_real_df = pd.DataFrame(list(nonsan_connector.query(sql)), columns=["FCST_TM",
                                                        "sum(tbl_inverter_min.KWD)", "avg(tbl_kma_min.intemp)",
                                                        "avg(tbl_kma_min.outtemp)", "avg(tbl_kma_min.insolS)"])
    nonsan_real_df.insert(0, "Coordinates", [str((36.149019, 127.176031)) for i in range(nonsan_real_df.shape[0])], True)
    merged_real_df = jeju_real_df.append(nonsan_real_df)

    joined_df = pd.merge(left=nwp_df, right=merged_real_df, how="left", on=["FCST_TM", "Coordinates"])
    joined_df = joined_df.fillna(0)
    return joined_df
    # joined_df = joined_df.iloc[:, 4:]

    # joined_df.to_excel("/home/jhpark/data_files/training_base_left_plus1hour.xlsx")


def model_create(model_name):
    base_df = pd.read_excel("/home/jhpark/data_files/training_base_left_plus1hour.xlsx")
    df = np.array(base_df)
    df_len = df.shape[0]
    training_data_rate = 0.8
    training_index = int(df_len*training_data_rate)

    training_X = df[:training_index, :-1]
    training_Y = df[:training_index, -1]

    prediction_X = df[training_index:, :-1]
    real_Y = df[training_index:, -1]

    model = keras.Sequential()
    model.add(keras.layers.Dense(15, input_dim=15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.GaussianDropout(7))
    # model.add(keras.layers.MaxoutDense(7))
    # model.add(keras.layers.GaussianDropout(7))
    # model.add(keras.layers.MaxoutDense(7))
    # model.add(keras.layers.GaussianDropout(7))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(14))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(13))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(12))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(11))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(10))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(9))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(8))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(7))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(6))
    model.add(keras.layers.MaxoutDense(5))
    model.add(keras.layers.MaxoutDense(5))
    model.add(keras.layers.MaxoutDense(4))
    model.add(keras.layers.MaxoutDense(4))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(3))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    model.add(keras.layers.MaxoutDense(2))
    # model.add(keras.layers.GaussianDropout(7))
    # model.add(keras.layers.MaxoutDense(15))
    # model.add(keras.layers.MaxoutDense(15))
    # model.add(keras.layers.MaxoutDense(15))
    # model.add(keras.layers.MaxoutDense(15))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    # model.add(keras.layers.Dense(15, activation="relu"))
    model.add(keras.layers.Dense(1, activation="linear"))
    model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

    model.fit(training_X, training_Y, epochs=150)
    model.save("data_file/model_files/"+model_name)


def model_evaluation(model_name, training_rate, same_with_training=False):
    base_df = pd.read_excel("/home/jhpark/data_files/training_base_left_plus1hour.xlsx")
    df = np.array(base_df)
    df_len = df.shape[0]
    training_data_rate = training_rate
    training_index = int(df_len*training_data_rate)

    if same_with_training == False:
        prediction_X = df[training_index:, :-1]
        real_Y = df[training_index:, -1]
    else:
        prediction_X = df[:training_index, :-1]
        real_Y = df[:training_index, -1]

    model = keras.models.load_model("data_file/model_files/"+model_name)
    prediction = model.predict(prediction_X)

    prediction = np.asarray([x[0] for x in prediction])

    nape_list = np.abs(prediction - real_Y)/99
    nmape = np.average(nape_list)
    print(nmape)

    # plt.plot(prediction)
    # plt.plot(real_Y)
    # plt.show()


training_rate = 0.8


if __name__ == "__main__":
    model_name = "0930newmodel4.h5"
    # base_file_create()
    model_create(model_name)
    model_evaluation(model_name, training_rate, same_with_training=False)
