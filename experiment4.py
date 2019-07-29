import ftplib
import pygrib
import datetime
from math import *
from haversine import *
import matplotlib.pyplot as plt
import string
import random
from Load_data import *
from data_manipulation import *
import pandas as pd
import time


temp_file = pygrib.open("/home/jhpark/NWP/l015_v070_erlo_unis_h015.2019031212.gb2")

a = temp_file[1].values
print(a)