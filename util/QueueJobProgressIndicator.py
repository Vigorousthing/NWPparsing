import multiprocessing
import time
from util import Visualizer


class QueueJobProgressIndicator(multiprocessing.Process):
    def __init__(self, container):
        super(QueueJobProgressIndicator, self).__init__()
        self.container = container
        self.visualizer = Visualizer()
        self.original_qsize = container.qsize()

    def run(self):
        while not self.container.empty():
            self.visualizer.print_progress(self.original_qsize - self.container.qsize(), self.original_qsize,
                                      'Value Extract Progress:',
                                      'Complete', 1, 50)
            time.sleep(3)
