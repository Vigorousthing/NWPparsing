import nwp_parsing


def remove_files(ftp_accessor, data_type, fold_type, time_interval, horizon_interval=[0, 36]):
    ftp_accessor.data_type_setting(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
    ftp_accessor.set_file_names()
    ftp_accessor.check_total_size_of_files()
    ftp_accessor.remove_from_local_pc()


def extract_variable_values(ftp_accessor, data_type, fold_type, time_interval,
                            var_list, nearest_type, point,
                            output_file_name="experimental", horizon_interval=[0, 36]):
    ftp_accessor.data_type_setting(data_type, fold_type, time_interval, horizon_interval=horizon_interval)
    ftp_accessor.set_file_names()
    ftp_accessor.check_total_size_of_files()
    ftp_accessor.save_file_from_ftp_server()
    ftp_accessor.extract_variable_values("tarining", var_list, nearest_type, point, "experimental")
    ftp_accessor.close()

