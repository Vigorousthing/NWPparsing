from util.Visualizer import *
from data_accessors.MongoDbConnector import *
import time
from nwp_object.NwpFile import *

all_plant_id_list = "all"
plant_location_list = InputConverter().vpp_compx_id_to_coordinates(
    all_plant_id_list, get_site_info_df())

print(plant_location_list)

plant_id_list1 = ["P31S2105", "P31S51157", "P61S2102", "P61S31530",
                  "P41S21482"]
plant_location_list1 = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list1, get_site_info_df()
)

plant_id_list2 = ["P31S51040", "P61S31210", "P61S31453", "P61S31550",
                  "P64S52120"]
plant_location_list2 = InputConverter().vpp_compx_id_to_coordinates(
    plant_id_list2, get_site_info_df()
)

visualizer = Visualizer()
visualizer.plot_some_points(plant_location_list, plant_location_list1,
                            plant_location_list2, marker_size=3)

