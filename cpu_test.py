#
# import multiprocessing
#
# queue = multiprocessing.Array("i", 1)
#
#
# class Adder(multiprocessing.Process):
#     def __init__(self, queue):
#         super(Adder, self).__init__()
#         self.obj = queue
#
#     def run(self):
#         while self.obj[0] < 1000000:
#             self.obj[0] += 1
#
# import time
# start = time.time()
#
# for i in range(50):
#     Adder(queue).run()
#
# end = time.time()
#
# print(end - start)



import pandas as pd
