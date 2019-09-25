from data_extract.IndividualDataCollector import IndividualDataCollector


class DataOrganizer:
    def __init__(self, grid_analyzer, files_container):
        self.total_df = None

        self.grid_analyzer = grid_analyzer
        self.files_container = files_container

        self.individual_collector = {}

    def data_collect(self, num_of_indiv_collector):
        for i in range(num_of_indiv_collector):
            self.individual_collector[i] = IndividualDataCollector(self.grid_analyzer, self.files_container)
            self.individual_collector[i].start()
        for i in range(num_of_indiv_collector):
            self.individual_collector[i].join()

        self.total_df = self.files_container.output_container.get()
        for i in range(1, num_of_indiv_collector):
            self.total_df = self.total_df.append(self.files_container.output_container.get())

        # for i in range(num_of_indiv_collector):
        #     self.individual_collector[i].close()
        # self.total_df = self.individual_collector[0].df
        # for i in range(1, num_of_indiv_collector):
        #     self.total_df = self.total_df.append(self.individual_collector[i].df)
        return self.total_df