import multiprocessing
import datetime
import re


class FilesContainer:
    def __init__(self, container_class, fold_type, location_points, variables):
        self.type = container_class
        self.fold_type = fold_type
        self.location_points = location_points
        self.variables = variables

        # self.current_time = None

        self.start_time = None
        self.end_time = None

        self.container = multiprocessing.Manager().Queue()
        self.output_container = multiprocessing.Manager().Queue()

        self.filename_list = []

    def generate_base_files(self, time_interval):
        self.start_time, self.end_time = self.time_alignment(time_interval)
        current_time = self.start_time
        while current_time <= self.end_time:
            date_string = re.sub('[^A-Za-z0-9]+', '', str(current_time))[:-4]
            for horizon in range(self.type.full_horizon + 1):
                if horizon % self.type.prediction_interval == 0:
                    file_object = self.type(self.fold_type, horizon, date_string, self.location_points, self.variables)
                    self.container.put(file_object)
                    self.filename_list.append(file_object.name)
            current_time = current_time + datetime.timedelta(hours=6)

    def generate_base_prediction_files(self, current_time):
        # self.filename_list = []
        # input parameter type can be changed to datetime object
        current_time = datetime.datetime.strptime(current_time, "%Y-%m-%d %H")\
                       - datetime.timedelta(hours=9)
        dif_from_last_prediction = current_time.hour % 6
        prediction_start = current_time - datetime.timedelta(hours=dif_from_last_prediction)
        new_horizon = self.type.full_horizon - dif_from_last_prediction

        date_string = re.sub('[^A-Za-z0-9]+', '', str(prediction_start))[:-4]
        for horizon in range(new_horizon + 1):
            if horizon % self.type.prediction_interval == 0:
                file_object = self.type(self.fold_type, horizon + dif_from_last_prediction,
                                        date_string, self.location_points,
                                        self.variables)
                self.container.put(file_object)
                self.filename_list.append(file_object.name)
        # self.filename_list.append(filename_list)

    @staticmethod
    def time_alignment(time_interval):
        start_time = datetime.datetime.strptime(time_interval[0], "%Y-%m-%d %H") - datetime.timedelta(hours=9)
        end_time = datetime.datetime.strptime(time_interval[1], "%Y-%m-%d %H") - datetime.timedelta(hours=9)
        if start_time.hour % 6 != 0:
            start_time = start_time + datetime.timedelta(hours=(6 - (start_time.hour % 6)))
        if end_time.hour % 6 != 0:
            end_time = end_time - datetime.timedelta(hours=end_time.hour % 6)
        return start_time, end_time
