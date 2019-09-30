import CONSTANT
from data_extract.DataOrganizer import DataOrganizer
from util.QueueJobProgressIndicator import QueueJobProgressIndicator
import keras
import numpy as np
import pandas as pd
import datetime


def create_training_dataset():
    pass


def amend_prediction_df(prediction_df, prediction, current_time):
    prediction_df["CRTN_TM"] = datetime.datetime.strptime(current_time, "%Y-%m-%d %H")
    prediction_df["new_horizon"] = prediction_df.apply(
        lambda row: int(
                    (row.FCST_TM - row.CRTN_TM).days * 24 +
                    (row.FCST_TM - row.CRTN_TM).seconds / 3600
                    ),
                    axis=1)
    prediction_df["prediction"] = prediction
    prediction_df = prediction_df.drop(columns=["horizon"])
    return prediction_df


def merge_two_dfs(join_key_list, df1, df2):
    joined_df = pd.merge(left=df1, right=df2,
                         how="left", on=join_key_list)
    joined_df = joined_df.fillna(0)
    return joined_df


def create_current_prediction(container, ftp_accessor, analyzer, current_time, model_name):
    container.generate_base_prediction_files(current_time)
    filename_list = container.filename_list

    if not ftp_accessor.check_connection():
        ftp_accessor.reconnect()

    ftp_accessor.download_files(filename_list, container.type.nwp_type)

    progress_check = QueueJobProgressIndicator(container.container)
    progress_check.start()

    master = DataOrganizer(analyzer, container)
    df = master.data_collect(CONSTANT.num_of_process)
    input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "Coordinates"])
    prediction_df = df.drop(columns=container.variables)

    model = keras.models.load_model(CONSTANT.model_path + model_name)
    prediction = model.predict(np.array(input_df))

    return amend_prediction_df(prediction_df, prediction, current_time)


def create_interval_prediction(container, ftp_accessor, time_interval, prediction_type):
    start_time, end_time = container.time_alignment(time_interval)
    current_time = start_time
    if prediction_type == "daily":
        time_step = 24
    else:
        time_step = 6

    # download
    download_set = {None}
    while current_time <= end_time:
        container.generate_base_prediction_files(current_time)
        download_set.union(set(container.filname_list))
        current_time += datetime.timedelta(hours=time_step)
    ftp_accessor.download_files(download_set, container.type.nwp_type)

    current_time = start_time
    while current_time <= end_time:

        container.generate_base_prediction_files(current_time)
        download_set.union(set(container.filname_list))
        current_time += datetime.timedelta(hours=time_step)
