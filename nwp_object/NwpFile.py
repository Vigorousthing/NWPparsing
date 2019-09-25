import CONSTANT
import datetime
import pandas as pd


class NwpFiles:
    full_horizon = None
    prediction_interval = None
    nwp_type = None
    prefix = None
    info_file_name = None
    nwp_var_info = None

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        self.name = "{}_{}_h{}.{}.gb2".format(self.prefix, fold, str(horizon).zfill(3), crtn_tm)
        self.crtn_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H")
        self.fcst_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H") + datetime.timedelta(hours=horizon)

        self.horizon = horizon

        self.probable_crtn_tm = {}

        self.location_points = location_points
        self.variables = variables

        # self.set_property(fold, horizon, crtn_tm)
        self.generate_probable_crtn_tm()

    # def set_property(self, fold, horizon, crtn_tm):
    #     self.name = self.name.format(self.prefix, fold, str(horizon).zfill(3), crtn_tm)
    #     self.crtn_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H")
    #     self.fcst_tm = datetime.datetime.strptime(crtn_tm, "%Y%m%d%H") + datetime.timedelta(hours=horizon)

    def generate_probable_crtn_tm(self):
        for i in range(6):
            self.probable_crtn_tm[i] = self.crtn_tm + datetime.timedelta(hours=i)


class LdapsFile(NwpFiles):
    full_horizon = 48
    prediction_interval = 1
    nwp_type = "LDAPS"
    prefix = "l015_v070_erlo"
    info_file_name = CONSTANT.ldaps_variable_index_file_name
    nwp_var_info = pd.read_excel(CONSTANT.setting_file_path+info_file_name)

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        super(LdapsFile, self).__init__(fold, horizon, crtn_tm, location_points, variables)


class RdapsFile(NwpFiles):
    full_horizon = 87
    prediction_interval = 3
    nwp_type = "RDAPS"
    prefix = "g120_v070_erea"
    info_file_name = CONSTANT.rdaps_variable_index_file_name
    nwp_var_info = pd.read_excel(CONSTANT.setting_file_path+info_file_name)

    def __init__(self, fold, horizon, crtn_tm, location_points, variables="all"):
        super(RdapsFile, self).__init__(fold, horizon, crtn_tm, location_points, variables)





