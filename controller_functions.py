import CONSTANT
from data_extract.DataOrganizer import DataOrganizer
import keras
import numpy as np


def create_training_dataset():
    pass


def create_prediction(container, ftp_accessor, analyzer, current_time, model_name):
    container.generate_base_prediction_files(current_time)
    filename_list = container.filename_list

    if not ftp_accessor.check_connection():
        ftp_accessor.reconnect()

    ftp_accessor.download_files(filename_list, container.type.nwp_type)

    master = DataOrganizer(analyzer, container)
    df = master.data_collect(CONSTANT.num_of_process)
    input_df = df.drop(columns=["CRTN_TM", "FCST_TM", "Coordinates"])
    prediction_df = df.drop(columns=container.variables)

    model = keras.models.load_model(CONSTANT.model_path + model_name)
    prediction = model.predict(np.array(input_df))

    prediction_df["prediction"] = prediction

    return prediction_df
