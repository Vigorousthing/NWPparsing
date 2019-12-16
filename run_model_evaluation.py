from controllers.training_maker import *
from controllers.model_makers import *
from nwp_object.NwpFile import *


model_name = ["vpp0_1017.h5", "vpp1_1017.h5",
              "vpp2_1017.h5", "vpp3_1017.h5",
              "vpp4_1017.h5"]
variable = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]


def eval_on_test_data_of_training_data(model_name_list):
    nonje_data = pd.read_excel(CONSTANT.data_file_path + "nonje_abb_base_new"
                                                         ".xlsx")
    vpp_data = pd.read_excel(CONSTANT.data_file_path + "vpp_each_base.xlsx")

    nonje_model_object = LdapsModelObject(np.array(nonje_data[variable]),
                                          np.array(nonje_data["real"]))
    nonje_model_object.set_exist_model("nonje_1016model.h5")
    nonje_model_object.split_training_data_for_eval(0.8)
    nonje_nmape = nonje_model_object.eval_model()

    print("on each training spot")
    print("nonje_model", nonje_nmape)

    for i, val in enumerate(model_name_list):
        temp_vpp_data = vpp_data[vpp_data.location_num == i]
        temp = LdapsModelObject(np.array(temp_vpp_data[variable]),
                                np.array(temp_vpp_data["production"]))
        temp.set_exist_model(val)
        temp.split_training_data_for_eval(0)
        vpp_each_nmape = temp.eval_model()
        print(i, "th model", vpp_each_nmape)


def eval_on_cross_training_site(model_name_list):
    nonje_data = pd.read_excel(CONSTANT.data_file_path + "nonje_abb_base_new"
                                                         ".xlsx")
    vpp_data = pd.read_excel(CONSTANT.data_file_path + "vpp_each_base.xlsx")
    print("on cross training spot")
    # nonje model predicts vpp training sites
    for i in range(5):
        temp_vpp_data = vpp_data[vpp_data.location_num == i]
        temp_model_ob = LdapsModelObject(
            np.array(temp_vpp_data[variable]),
            np.array(temp_vpp_data["production"]))
        temp_model_ob.set_exist_model("nonje_1016model.h5")
        temp_model_ob.split_training_data_for_eval(0.8)
        nonje_nmape = temp_model_ob.eval_model()
        print("nonje_model on {}th site".format(i), nonje_nmape)

    vpp_model_ob = LdapsModelObject(np.array(nonje_data[variable]),
                                    np.array(nonje_data["real"]))
    vpp_model_ob.split_training_data_for_eval(0)
    for i, val in enumerate(model_name_list):
        vpp_model_ob.set_exist_model(val)
        vpp_each_nmape = vpp_model_ob.eval_model()
        print(i, "th vpp model on nonje site", vpp_each_nmape)


def eval_on_third_party_data(model_name_list):
    interval = [2019111800, 2019112500]
    site_id = ["P31S51040", "P61S31210", "P61S31453", "P61S31550", "P64S52120"]
    vars = ["NDNSW", "HFSFC", "TMP", "RH", "TMP-SFC"]
    training_maker = VppTraining(LdapsFile, "unis", interval, site_id, vars)
    data = training_maker.create_training_data_ldaps("thirdparty_test_nwp1125")
    data = data[variable + ["production", "location_num"]]

    data = data[data.location_num == 4]

    nonje_data = data
    # nonje_data = data[data.location_num == 2]

    free_var = np.array(nonje_data[variable])
    dpnt_var = np.array(nonje_data["production"])

    nonje_model_object = LdapsModelObject(free_var, dpnt_var)
    nonje_model_object.set_exist_model("nonje_1016model.h5")
    nonje_model_object.split_training_data_for_eval(0)
    nonje_nmape = nonje_model_object.eval_model()
    print("on apart from training spot")
    print("nonje_model", nonje_nmape)

    for i, val in enumerate(model_name_list):
        # temp_vpp_data = data[data.location_num == i]
        temp_vpp_data = data

        temp = LdapsModelObject(np.array(temp_vpp_data[variable]),
                                np.array(temp_vpp_data["production"]))
        temp.set_exist_model(val)
        temp.split_training_data_for_eval(0)
        vpp_each_nmape = temp.eval_model()
        print(i, "th model", vpp_each_nmape)


if __name__ == '__main__':
    # eval_on_test_data_of_training_data(model_name)
    print("---------------------")
    # eval_on_cross_training_site(model_name)
    print("---------------------")
    eval_on_third_party_data(model_name)
