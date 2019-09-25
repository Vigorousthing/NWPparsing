import numpy as np
from scipy import interpolate as spi
import pandas as pd

filename = "final.xlsx"

data = pd.read_excel("other_files/"+filename)

asos_list = data["asos"].tolist()
office_list = data["office"].tolist()
plant_list = data["plant"].tolist()

# location - 1:asos, 2:office, 3:plant
location = 2

if location == 1:
    x_list = asos_list
    y_list = asos_list
    name = "asos_interpolation"
elif location == 2:
    x_list = office_list
    y_list = office_list
    name = "office_interpolation"
elif location == 3:
    x_list = plant_list
    y_list = plant_list
    name = "plant_interpolation"

x = np.linspace(0, 100, len(x_list))
y = y_list
fq = spi.interp1d(x, y, kind="quadratic")

xint = np.linspace(x.min(), x.max(), (len(x_list)-1)*3+1)
yint = fq(xint)

np.savetxt("other_files/" + name + ".csv", yint, delimiter=",")