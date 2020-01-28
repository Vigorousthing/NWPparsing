import keras
import CONSTANT
from sklearn.svm import SVC
import pickle


class ModelObject:
    def __init__(self, free_var_data=None, dpnt_var_data=None):
        self.original_input_free = free_var_data
        self.original_input_dpnt = dpnt_var_data

        self.training_input_free = free_var_data
        self.training_input_dpnt = dpnt_var_data
        self.eval_input_free = None
        self.eval_input_dpnt = None

        self.split_training_data_for_eval()

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
        self.model = SVC(kernel="linear")
        self.model.fit(self.training_input_free, self.training_input_dpnt)

        with open(CONSTANT.model_path + model_name, "wb") as f:
            pickle.dump(self.model, f)
        # self.model.save(CONSTANT.model_path + model_name)
        self.eval_model()

    def set_exist_model(self, model_name):
        self.model = keras.models.load_model(CONSTANT.model_path + model_name)

    def set_training_data(self, free_var_data, dpnt_var_data):
        self.training_input_free = free_var_data
        self.training_input_dpnt = dpnt_var_data

    def set_eval_data(self, free_var_data, dpnt_var_data):
        self.eval_input_free = free_var_data
        self.eval_input_dpnt = dpnt_var_data

    def split_training_data_for_eval(self, training_rate=0.8):
        if self.original_input_free is None or self.original_input_dpnt is \
                None:
            return
        df_len = self.original_input_free.shape[0]
        idx = int(df_len*training_rate)

        self.eval_input_free = self.original_input_free[idx:, :]
        self.eval_input_dpnt = self.original_input_dpnt[idx:]

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


class LdapsModelObject(ModelObject):
    def __init__(self, free_var_data=None, dpnt_var_data=None):
        super(LdapsModelObject, self).__init__(free_var_data, dpnt_var_data)
        self.output_num = 1
        pass

    def eval_model(self):
        num = 0
        print(self.make_prediction(self.eval_input_free))
        # for i, val in enumerate(self.make_prediction(self.eval_input_free)):
        #     num += abs(val[0] - self.eval_input_dpnt[i])/99
        for i, val in enumerate(self.make_prediction(self.eval_input_free)):
            num += abs(val - self.eval_input_dpnt[i])/99
        nmape = num/len(self.make_prediction(self.eval_input_free))
        print(nmape)
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
        print(nmape)
        return nmape


if __name__ == '__main__':

    pass
