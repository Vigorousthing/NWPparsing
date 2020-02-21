from controllers.training_maker import *
from util.input_converter import *
from nwp_object.NwpFile import *


# vpp_site_id = ["P31S51040", "P61S31210", "P61S31453", "P61S31550",
#                "P64S52120"]
variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]

# coordinates = CONSTANT.jenon_coordinates
# coordinates = CONSTANT.garage_coordinates

# time_interval = InputConverter.time_interval_from_m_w(year, month, week_th)
# save_filename = InputConverter().save_filename_for_signiture_location(
#     time_interval, coordinates)


def iterate_inside_month(y, m):
    coordinates_list = [CONSTANT.jenon_coordinates,
                        CONSTANT.garage_coordinates]
    for w in range(1, 6):
        time_interval = InputConverter.time_interval_from_m_w(y, m, w)
        for coordinates in coordinates_list:
            save_filename = InputConverter().\
                save_filename_for_signiture_location(
                time_interval, coordinates)

            nwp_extract = TrainingDataMaker(LdapsFile, "unis", time_interval,
                                            coordinates, variables)
            nwp_extract.create_nwp_checkpoint(save_filename, remove=False)
        nwp_extract.ftp_accessor.remove_from_local_pc(
            nwp_extract.container.filename_list)


def extarct_from_m_w(y, m, w_th):
    coordinates_list = [CONSTANT.jenon_coordinates,
                        CONSTANT.garage_coordinates]
    time_interval = InputConverter.time_interval_from_m_w(y, m, w_th)

    for coordinates in coordinates_list:
        save_filename = InputConverter().save_filename_for_signiture_location(
            time_interval, coordinates)
        nwp_extract = TrainingDataMaker(LdapsFile, "unis", time_interval,
                                        coordinates, variables)
        nwp_extract.create_nwp_checkpoint(save_filename, remove=False)


if __name__ == '__main__':
    year = 2019
    month = 11

    # iterate_inside_month(year, month)
    extarct_from_m_w(year, month, 5)

    # nwp_extract = TrainingDataMaker(LdapsFile, "unis", time_interval,
    #                                 coordinates, variables)
    # start = datetime.datetime.now()
    # nwp_extract.create_nwp_checkpoint(save_filename, remove=False)
    # end = datetime.datetime.now()
    # print(end-start, ": lapsed")
    pass


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
