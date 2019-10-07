from data_extract.IndividualDataCollector import IndividualDataCollector


class DataOrganizer:
    def __init__(self, grid_analyzer, files_container):
        self.total_df = None

        self.grid_analyzer = grid_analyzer
        self.files_container = files_container

        self.individual_collector = {}

    def data_collect(self, num_of_indiv_collector):
        for i in range(num_of_indiv_collector):
            self.individual_collector[i] = IndividualDataCollector(
                self.grid_analyzer, self.files_container)
            self.individual_collector[i].start()
        for i in range(num_of_indiv_collector):
            self.individual_collector[i].join()

        print(self.files_container.output_container.qsize())

        # change to while not empty
        df = self.files_container.output_container.get()
        while not self.files_container.output_container.empty():
            df = df.append(self.files_container.output_container.get(),
                           sort=False)
        return df
