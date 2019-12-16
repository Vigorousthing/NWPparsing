import keras
import CONSTANT
import numpy as np


class ModelObject:
    def __init__(self, free_var_data=None, dpnt_var_data=None):
        self.training_input_free = free_var_data
        self.training_input_dpnt = dpnt_var_data
        self.eval_input_free = None
        self.eval_input_dpnt = None

        self.output_num = None

        self.model = keras.Sequential()

    def eval_model(self):
        raise NotImplementedError

    def create_new_model(self, model_name, epoch):
        self.split_training_data_for_eval()
        self.compile_model(self.training_input_free.shape[1],
                           self.output_num)
        self.fit_data(epoch)
        self.model.save(CONSTANT.model_path + model_name)
        self.eval_model()

    def set_exist_model(self, model_name):
        self.model = keras.models.load_model(CONSTANT.model_path + model_name)

    def set_training_data(self, free_var_data, dpnt_var_data):
        self.training_input_free = free_var_data
        self.training_input_dpnt = dpnt_var_data

    def set_eval_data(self, free_var_data, dpnt_var_data):
        self.eval_input_free = free_var_data
        self.eval_input_dpnt = dpnt_var_data

    def split_training_data_for_eval(self, rate=0.8):
        df_len = self.training_input_free.shape[0]
        idx = int(df_len*rate)

        self.eval_input_free = self.training_input_free[idx:, :]
        self.eval_input_dpnt = self.training_input_dpnt[idx:]

        self.training_input_free = self.training_input_free[:idx, :]
        self.training_input_dpnt = self.training_input_dpnt[:idx]

    def make_prediction(self, free_var_input):
        return self.model.predict(free_var_input)

    def compile_model(self, input_num, output_num=1):

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


class LdapsModelObject(ModelObject):
    def __init__(self, free_var_data=None, dpnt_var_data=None):
        super(LdapsModelObject, self).__init__(free_var_data, dpnt_var_data)
        self.output_num = 1
        pass

    def eval_model(self):
        num = 0
        for i, val in enumerate(self.make_prediction(self.eval_input_free)):
            num += abs(val[0] - self.eval_input_dpnt[i])/99

        nmape = num/len(self.make_prediction(self.eval_input_free))
        return nmape


class RdapsModelObject(ModelObject):
    def __init__(self, free_var_data=None, dpnt_var_data=None):
        super(RdapsModelObject, self).__init__(free_var_data, dpnt_var_data)
        self.output_num = 3

    def eval_model(self):
        prediction = self.make_prediction(self.eval_input_free)
        num = 0
        for idx, arr in enumerate(self.eval_input_dpnt):
             for idx2, ele in enumerate(arr):
                num += abs(ele - prediction[idx][idx2])
        nmape = num/(99*(3*len(prediction)))
        return nmape


if __name__ == '__main__':

    pass
