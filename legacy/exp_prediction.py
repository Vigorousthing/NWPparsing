import pandas as pd
import numpy as np
import keras
import matplotlib.pyplot as plt


dataset = pd.read_excel("/home/jhpark/experiment_files/524predictioninput.xlsx")
df = np.array(dataset)

prediction_X = df[:, :7]
# real_Y = df[:, 7]

model = keras.models.load_model("510prediction.h5")
prediction = model.predict(prediction_X)
# print prediction
prediction = np.asarray([x[0] for x in prediction])
print(prediction.shape)
np.savetxt("524prediction.csv", prediction, delimiter=",")