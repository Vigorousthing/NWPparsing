from controllers.real_data_maker import *
from data_accessors.FtpAccessor import *
from util.QueueJobProgressIndicator import *
from nwp_object.FilesContainer import *
from util.Visualizer import Visualizer
from util.NwpGridAnalyzer import NwpGridAnalyzer
from controllers.model_makers import *
from data_extract.DataOrganizer import *
import numpy as np
import time


class TrainingDataMaker:
    def __init__(self, file_type, fold_type, time_interval,
                 location_coordinate_list, variables):
        self.file_type = file_type
        self.fold_type = fold_type
        self.time_interval = time_interval
        self.variables = variables
        self.location_list = location_coordinate_list

        self.ftp_accessor = FtpAccessor(CONSTANT.ftp_ip, CONSTANT.ftp_id,
                                        CONSTANT.ftp_pw)
        self.mongo_connector = MongodbConnector("sites", "production")
        self.nwp_checkpoint_filename = None

        self.analyzer = NwpGridAnalyzer()
        self.visualizer = Visualizer()
        self.input_converter = InputConverter()
        self.container = FilesContainer(file_type, fold_type,
                                        self.location_list, variables)
        self.master = DataOrganizer(self.analyzer, self.container)

        self.queue_job_checker = None
        self.real_maker = None

    def create_nwp_checkpoint(self, save_df_name, remove=True):
        df = None
        # 1. type conversion : int(ex: 2019101100) to datetime object
        converted_interval = self.input_converter.time_interval_conversion(
            self.time_interval)

        # 2. split time interval for
        time_interval_list = self.split_time(converted_interval)

        # 3. loop split time interval
        for i, time_interval in enumerate(time_interval_list):
            # 3-1 initialize container
            self.container.initialize_except_output()
            # 3-2 fill container with nwp objects
            self.container.generate_base_files(time_interval)

            # 3-3 reconnect ftp connection in each iteration.
            if not self.ftp_accessor.check_connection():
                self.ftp_accessor.reconnect()

            # 3-4 download files in container
            print(i+1, "th iteration / total :", len(time_interval_list))
            self.ftp_accessor.download_files(self.container.filename_list,
                                             self.container.type.nwp_type)

            # 3-5 set job progress check indicator
            self.queue_job_checker = QueueJobProgressIndicator(
                self.container.container)
            self.queue_job_checker.start()

            start = time.time()

            # 3-6 extract data for each time interval
            temp_df = self.master.data_collect(CONSTANT.num_of_process)
            temp_df.to_excel(CONSTANT.data_file_path + save_df_name +
                             "temp_file_" + str(i) + ".xlsx")
            if i == 0:
                df = temp_df
            else:
                df = df.append(temp_df)

            end = time.time()
            if remove is True:
                self.ftp_accessor.remove_from_local_pc(
                    self.container.filename_list)
            print("passed in {}th iteration : ".format(i), end - start)
            self.queue_job_checker.terminate()

            #join!!!!!

        df.to_excel(CONSTANT.data_file_path + "{}.xlsx".
                    format(save_df_name))

    def create_nwp_checkpoint_from_files_in_directory(self, path):
        # 1. fill container with files
        self.container.create_training_data_files_from_directory(path)

        # 2. set job progress check indicator
        self.queue_job_checker = QueueJobProgressIndicator(
            self.container.container)
        self.queue_job_checker.start()

        # 3. extract data for each time interval
        df = self.master.data_collect(CONSTANT.num_of_process)
        # df.to_excel(
        #     CONSTANT.data_file_path + "temp_file_" + str(i) +
        #     ".xlsx")
        self.queue_job_checker.terminate()
        return df

    def create_real(self):
        return self.real_maker.query_real_data()

    def create_training_data_ldaps(self, checkpoint_filename):
        nwp_df = pd.read_excel(
            CONSTANT.data_file_path + checkpoint_filename + ".xlsx")
        real_df = self.create_real()

        result = pd.merge(nwp_df, real_df, how="inner", on=["location_num",
                                                            "FCST_TM"])
        result = result.drop(columns=["Unnamed: 0", "lat_x", "lon_x",
                                      "lat_y", "lon_y", "Coordinates"])
        return result

        # return np.array(result[self.variables]), result["production"]

    def create_training_data_rdaps(self, checkpoint_filename):
        nwp_df = pd.read_excel(
            CONSTANT.data_file_path + checkpoint_filename + ".xlsx")
        real_df = self.create_real()
        input_df = nwp_df[self.variables]

        output_list = []
        for idx, row in nwp_df.iterrows():
            location_num = row.location_num
            fcst_tm = row.FCST_TM

            temp_list = []
            for i in range(self.file_type.prediction_interval):
                new_fcst_tm = fcst_tm - datetime.timedelta(
                    hours=self.file_type.prediction_interval - i)
                real_val = real_df[(real_df["FCST_TM"] == new_fcst_tm) &
                                   (real_df["location_num"] == location_num)]
                try:
                    temp_list.append(real_val.production.values[0])
                except IndexError:
                    temp_list.append(0)
            output_list.append(temp_list)
        return np.array(input_df), np.array(output_list)

    @staticmethod
    def split_time(converted_time_interval):
        time_interval_list = []
        start, end = converted_time_interval[0], converted_time_interval[1]

        while start <= end:
            temp_list = [start]

            start += datetime.timedelta(days=
                                        CONSTANT.
                                        length_of_time_interval_for_training)
            # start -= datetime.timedelta(hours=1)

            if start <= end:
                temp_list.append(start)
                # start += datetime.timedelta(hours=1)
            else:
                temp_list.append(end)

            time_interval_list.append(temp_list)

            if int((end-start).total_seconds()) == 0:
                break

        return time_interval_list


class VppTraining(TrainingDataMaker):
    def __init__(self, file_type, fold_type, time_interval, plant_id_list,
                 variables):
        super(VppTraining, self).__init__(file_type, fold_type,
                                          time_interval, InputConverter().vpp_compx_id_to_coordinates(plant_id_list, get_site_info_df()),
                                          variables)
        self.real_maker = VppRealMaker(self.time_interval, plant_id_list)


class JenonTraining(TrainingDataMaker):
    def __init__(self, file_type, fold_type, time_interval, variables):
        super(JenonTraining, self).__init__(file_type, fold_type,
                                            time_interval,
                                            [CONSTANT.jenon_coordinates[0],
                                             CONSTANT.jenon_coordinates[1]],
                                            variables)
        self.real_maker = JenonRealMaker(self.time_interval)


if __name__ == '__main__':
    from nwp_object.NwpFile import *

    time_interval = [2019111800, 2019112500]
    vpp_site_id = ["P31S51040", "P61S31210", "P61S31453", "P61S31550",
                   "P64S52120"]
    variables = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]

    maker1 = VppTraining(LdapsFile, "unis", time_interval, vpp_site_id,
                         variables)
    # maker1.create_nwp_checkpoint("thridparty_test_nwp1125", remove=False)
    free_var, dpnt_var = maker1.create_training_data_ldaps(
        "thridparty_test_nwp1125")



    # maker2 = JenonTraining(RdapsFile, "unis", [2019080100, 2019093023],
    #                        ["NDNSW", "XGWSS", "YGWSS", "LLRIB", "HFSFC",
    #                         "TMOFS", "SHFO", "SUBS", "TMP", "TMIN",
    #                         "TMAX", "UCAPE", "UPCIN", "LCDC", "MCDC",
    #                         "HCDC", "TCAR", "TCAM", "TMP-SFC", "PRES"])

    # maker1.create_nwp_checkpoint("ldaps_checkpoint")
    # maker2.create_nwp_checkpoint("rdaps_checkpoint09")

    # df = maker1.create_training_data_ldaps("ldaps_checkpoint")
    # lists = maker2.create_training_data_rdaps("rdaps_checkpoint0809")
    #
    # modelob = RdapsModelObject(lists[0], lists[1])
    # modelob.create_new_model("rdaps.h5", 30)

