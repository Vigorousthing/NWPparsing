import multiprocessing
import datetime
from util.input_converter import InputConverter


class FilesContainer:
    def __init__(self, container_class, fold_type,
                 location_points, variables="all"):
        self.type = container_class
        self.fold_type = fold_type
        self.location_points = location_points
        self.variables = variables

        self.start_time = None
        self.end_time = None
        self.prediction_time = None

        self.converter = InputConverter()

        self.container = multiprocessing.Manager().Queue()
        self.output_container = multiprocessing.Manager().Queue()
        self.filename_list = []

    def generate_base_files(self, time_interval):
        self.start_time, self.end_time = self.time_alignment(time_interval)
        current_time = self.start_time
        while current_time <= self.end_time:
            # date_string = re.sub('[^A-Za-z0-9]+', '', str(current_time))[:-4]
            for horizon in range(self.type.full_horizon + 1):
                if horizon % self.type.prediction_interval == 0:
                    file_object = self.type(self.fold_type, horizon,
                                            current_time, self.location_points,
                                            self.variables)
                    self.container.put(file_object)
                    self.filename_list.append(file_object.name)
            current_time = current_time + datetime.timedelta(hours=6)

    def generate_base_prediction_files(self, current_time):
        # input parameter type can be changed to datetime object
        current_time = self.converter.current_time_conversion(current_time) -\
                       datetime.timedelta(hours=9)
        self.filename_list = []

        dif_from_last_prediction = current_time.hour % 6
        prediction_start = current_time - \
            datetime.timedelta(hours=dif_from_last_prediction)
        new_horizon = self.type.full_horizon - dif_from_last_prediction

        # date_string = re.sub('[^A-Za-z0-9]+', '', str(prediction_start))[:-4]
        for horizon in range(new_horizon + 1):
            if horizon % self.type.prediction_interval == 0:
                file_object = self.type(self.fold_type,
                                        horizon + dif_from_last_prediction,
                                        prediction_start, self.location_points,
                                        self.variables)
                self.container.put(file_object)
                self.filename_list.append(file_object.name)

    def generate_real_time_prediction_files(self, ftp_accessor):
        # input parameter type can be changed to datetime object

        current_time = datetime.datetime.now() - datetime.timedelta(hours=9)
        self.filename_list = []

        dif_from_last_prediction = current_time.hour % 6
        prediction_start = current_time - \
                           datetime.timedelta(hours=dif_from_last_prediction)
        new_horizon = self.type.full_horizon - dif_from_last_prediction

        # date_string = re.sub('[^A-Za-z0-9]+', '', str(prediction_start))[:-4]
        for horizon in range(new_horizon + 1):
            if horizon % self.type.prediction_interval == 0:
                while True:
                    file_object = self.type(self.fold_type,
                                            horizon +
                                            dif_from_last_prediction,
                                            prediction_start,
                                            self.location_points,
                                            self.variables)
                    if ftp_accessor.existence_check(file_object.name) is True:
                        self.container.put(file_object)
                        self.filename_list.append(file_object.name)
                        break
                    elif horizon + dif_from_last_prediction \
                            > self.type.full_horizon:
                        print("there is no file for this fcst_tm")
                        break
                    else:

                        continue

    @staticmethod
    def time_alignment(time_interval):
        start_time = time_interval[0] - datetime.timedelta(hours=9)
        end_time = time_interval[1] - datetime.timedelta(hours=9)
        if start_time.hour % 6 != 0:
            start_time = start_time + datetime.timedelta(
                hours=(6 - (start_time.hour % 6)))
        if end_time.hour % 6 != 0:
            end_time = end_time - datetime.timedelta(hours=end_time.hour % 6)
        return start_time, end_time
