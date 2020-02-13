from controllers.training_maker import *
from util.input_converter import *

from nwp_object.NwpFile import *

time_interval = [2019100100, 2019103123]
# vpp_site_id = ["P31S51040", "P61S31210", "P61S31453", "P61S31550",
#                "P64S52120"]
variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]

# goduk / dobong / jichuk / gaehwa
garage_coordinates = [(37.566601, 127.168451), (37.701720, 127.052289),
                      (37.651369, 126.906272), (37.578967, 126.793614)]

if __name__ == '__main__':
    nwp_extract = TrainingDataMaker(LdapsFile, "unis", time_interval,
                                    garage_coordinates, variables)
    # maker1 = VppTraining(LdapsFile, "unis", time_interval, vpp_site_id,
    #                      variables)
    start = datetime.datetime.now()
    # maker1.create_nwp_checkpoint("speedtest_from_jhpark", remove=False)
    # maker1.create_training_data_ldaps("thridparty_test_nwp1125")
    nwp_extract.create_nwp_checkpoint("2019y10m_sgv_20200213",
                                      remove=False)
    end = datetime.datetime.now()
    print(end-start, ": lapsed")



# file_type = LdapsFile
# fold_type = "unis"
# time_interval = [2019102400, 2019102406]
# l_var = InputConverter.convert_to_variable_list("all", LdapsFile)
#
# nwp_checkpointer = TrainingDataMaker(file_type, fold_type, time_interval,
#                                      l_var)
# nwp_checkpointer.create_nwp_checkpoint(
#     str(time_interval[0]) + "to" + str(time_interval[1]))
#
#
