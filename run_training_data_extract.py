from controllers.training_maker import *
from util.input_converter import *

file_type = LdapsFile
fold_type = "unis"
time_interval = [2019102400, 2019102406]
l_var = InputConverter.convert_to_variable_list("all", LdapsFile)

nwp_checkpointer = TrainingDataMaker(file_type, fold_type, time_interval,
                                     l_var)
nwp_checkpointer.create_nwp_checkpoint(
    str(time_interval[0]) + "to" + str(time_interval[1]))


