from data_extract.IndividualDataCollector import IndividualDataCollector
from util.QueueJobProgressIndicator import QueueJobProgressIndicator


class DataOrganizer:
    def __init__(self, grid_analyzer, files_container):
        self.total_df = None

        self.grid_analyzer = grid_analyzer
        self.files_container = files_container

        self.individual_collector = {}

    def data_collect(self, num_of_indiv_collector):
        self.progress_check()
        for i in range(num_of_indiv_collector):
            self.individual_collector[i] = IndividualDataCollector(
                self.grid_analyzer, self.files_container)
            self.individual_collector[i].start()
        for i in range(num_of_indiv_collector):
            self.individual_collector[i].join()

        if self.files_container.output_container.empty():
            return

        df = self.files_container.output_container.get()
        while not self.files_container.output_container.empty():
            df = df.append(self.files_container.output_container.get(),
                           sort=False)
        return df

    def reset_container(self, files_container):
        self.files_container = files_container

    def progress_check(self):
        queue_job_checker = QueueJobProgressIndicator(
            self.files_container.container)
        queue_job_checker.start()

