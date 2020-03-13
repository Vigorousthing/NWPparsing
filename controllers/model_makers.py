import keras
import CONSTANT
from sklearn.svm import SVC, SVR
import pickle
import numpy as np
from controllers import eval_maker
from xgboost import *
from keras.layers import BatchNormalization, Dropout


class ModelObject:
    def __init__(self, original_df, model_input_var):
        self.original_df = original_df
        # self.original_df["original_real"] = self.original_df["real"]
        # self.original_df["real"] = self.original_df["real"] / (
        #         self.original_df["capacity"] / 99)

        self.eval_df_after_split = None
        self.model_input_var = model_input_var
        self.capacity = original_df["capacity"]

        self.original_input_free = np.array(self.original_df[
                                                self.model_input_var])
        self.original_input_dpnt = np.array(self.original_df["real"])

        self.training_input_free = np.array(self.original_df[
                                                self.model_input_var])
        self.training_input_dpnt = np.array(self.original_df["real"])

        self.eval_input_free = None
        self.eval_input_dpnt = None

        self.output_num = None

        self.model = None

    def eval_model(self):
        raise NotImplementedError

    def create_ann_model(self, model_name, epoch):
        self.model = keras.Sequential()
        self.compile_model_ann(self.training_input_free.shape[1],
                               self.output_num)
        self.fit_data(epoch)
        self.model.save(CONSTANT.model_path + model_name)
        self.eval_model()

    def create_svr_model(self, model_name):
        self.model = SVR(kernel="linear")
        self.model.fit(self.training_input_free, self.training_input_dpnt)
        pickle.dump(self.model, open(CONSTANT.model_path + model_name, "wb"))
        self.eval_model()

    def create_xgb_model(self, model_name=None):
        # self.model = XGBRegressor()
        self.model = XGBRFRegressor(booster="gbtree",
                                    max_depth=10,
                                    )
        # self.model = XGBRFRegressor()

        self.model.fit(self.training_input_free, self.training_input_dpnt)
        self.eval_model()
        pass

    def set_exist_model(self, model_name):
        if model_name[-2:] == "h5":
            self.model = keras.models.load_model(CONSTANT.model_path + model_name)
        else:
            self.model = pickle.load(
                open(CONSTANT.model_path + model_name, "rb"))

    def set_training_data(self, free_var_data, dpnt_var_data):
        self.training_input_free = free_var_data
        self.training_input_dpnt = dpnt_var_data

    def set_eval_data(self, free_var_data, dpnt_var_data):
        self.eval_input_free = free_var_data
        self.eval_input_dpnt = dpnt_var_data

    def split_training_data_for_eval(self, training_rate=0.8):
        # if self.original_input_free is None or self.original_input_dpnt is \
        #         None:
        #     return

        df_len = self.original_input_free.shape[0]
        idx = int(df_len*training_rate)

        self.eval_df_after_split = self.original_df[idx:]

        self.eval_input_free = self.original_input_free[idx:, :]
        self.eval_input_dpnt = self.original_input_dpnt[idx:]
        self.capacity = self.capacity[idx:]

        self.training_input_free = self.original_input_free[:idx, :]
        self.training_input_dpnt = self.original_input_dpnt[:idx]

    def make_prediction(self, free_var_input):
        return self.model.predict(free_var_input)

    def compile_model_ann(self, input_num, output_num=1):
        self.model.add(keras.layers.Dense(input_num, input_dim=input_num,
                                          activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))
        self.model.add(keras.layers.Dense(input_num, activation="relu"))

        self.model.add(keras.layers.Dense(output_num, activation="linear"))

        self.model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])

    def fit_data(self, epoch):
        self.model.fit(self.training_input_free, self.training_input_dpnt,
                       epochs=epoch)


class LdapsModelObject(ModelObject, eval_maker.SimpleEval):
    def __init__(self, original_df, model_input_var):
        super(LdapsModelObject, self).__init__(original_df, model_input_var)
        self.output_num = 1

    def eval_model(self):
        num = 0
        # print(self.make_prediction(self.eval_input_free))
        # for i, val in enumerate(self.make_prediction(self.eval_input_free)):
        #     num += abs(val[0] - self.eval_input_dpnt[i])/99

        prediction = self.make_prediction(self.eval_input_free).ravel()
        self.eval_df_after_split["prediction"] = prediction

        return super(LdapsModelObject, self)._eval(self.eval_df_after_split)


        # prediction = np.multiply(prediction, self.capacity/99)

        # for i, val in enumerate(prediction):
        #     num += abs(val - self.eval_input_dpnt[i] * (
        #         self.capacity[i]/99)) / self.capacity[i]
        # for i, val in enumerate(prediction):
        #     num += abs(val - self.eval_input_dpnt[i]) / 612
        #
        # nmape = num/len(prediction)
        # print(nmape)
        # return nmape


class RdapsModelObject(ModelObject):
    def __init__(self, original_df, model_input_var):
        super(RdapsModelObject, self).__init__(original_df, model_input_var)
        self.output_num = 3

    def eval_model(self):
        prediction = self.make_prediction(self.eval_input_free)
        num = 0
        for idx, arr in enumerate(self.eval_input_dpnt):
             for idx2, ele in enumerate(arr):
                num += abs(ele - prediction[idx][idx2])
        nmape = num/(99*(3*len(prediction)))
        print(nmape)
        return nmape


if __name__ == '__main__':

    pass
