# import threading
# import time
# import random


# class myThread(threading.Thread):
#     def __init__(self, barrier):
#         threading.Thread.__init__(self)
#         self.barrier = barrier
#
#     def run(self):
#         print("thread {} working on something".format(threading.current_thread()))
#         time.sleep(random.randint(1, 4))
#         print("thread {} is joining {} waiting on barrier".format(threading.current_thread(), self.barrier.n_waiting))
#         self.barrier.wait()
#         print("barrier has been lifted, continuing with work")


# barrier = threading.Barrier(2)
# threads = []
# for i in range(5):
#     thread = myThread(barrier)
#     thread.start()
#     threads.append(thread)

# for t in threads:
#     t.join()


import threading
import queue
import random
import time


# def mySubscriber(queue):
#     while not queue.empty():
#         item = queue.get()
#         if item is None:
#             print("None")
#             break
#         print("{} removed {} from the queue".format(threading.current_thread(), item))
#         queue.task_done()
#         time.sleep(1)
#
#
# myQueue = queue.Queue()
# for i in range(10):
#     myQueue.put(i)
#
# print("Queue Populated")
#
# threads = []
# for i in range(4):
#     thread = threading.Thread(target=mySubscriber, args=(myQueue,))
#     thread.start()
#     threads.append(thread)
#
# for thread in threads:
#     thread.join()


# def mySubscriber(queue):
#     while not queue.empty():
#         item = queue.get()
#         if item is None:
#             break
#         print("{} removed {} from the queue".format(threading.current_thread(), item))
#         queue.task_done()
#         time.sleep(1)
#
#
# myQueue = queue.LifoQueue()
# for i in range(10):
#     myQueue.put(i)
#
# print("Queue Populated")
#
# threads = []
# for i in range(3):
#     thread = threading.Thread(target=mySubscriber, args=(myQueue,))
#     thread.start()
#     threads.append(thread)
#
# for thread in threads:
#     thread.join()
#
# print("Queue is empty")
#
# def mySubscriber(queue):
#     while not queue.empty():
#         item = queue.get()
#         if item is None:
#             break
#         print("{} removed {} from the queue".format(threading.current_thread(), item))
#         queue.task_done()
#         time.sleep(1)
#
#
# myQueue = queue.PriorityQueue()
# for i in range(5):
#     myQueue.put(i, i)
# for i in range(5):
#     myQueue.put(i, i)
#
# print("Queue Populated")
# threads = []
# for i in range(2):
#     thread = threading.Thread(target=mySubscriber, args=(myQueue,))
#     thread.start()
#     threads.append(thread)
#
# for thread in threads:
#     thread.join()
#
# print("Queue is empty")


# import unittest
#
# def simpleFunction(x):
#     return x + 1
#
# class SimpleFunctionTest(unittest.TestCase):
#
#     def setUp(self):
#         print("This is run before all of our tests have a chance to execute")
#
#     def tearDown(self):
#         print("This is run before all of our tests have a chance to execute")
#
#     def test_simple_function(self):
#         print("Testing that our function works with positive tests")
#         self.assertEqual(simpleFunction(2), 3)
#         self.assertEqual(simpleFunction(1234123),1234124)
#         self.assertEqual(simpleFunction(0), 1)
#
#
# if __name__ == '__main__':
#     unittest.main()

import sys
import threading
import time
# import queue

# def myThread(queue):
#     while True:
#         try:
#             time.sleep(2)
#             raise Exception("Exception Thrown In Child Thread {}".format(threading.current_thread()))
#         except:
#             queue.put(sys.exc_info())
#
#
# queue = queue.Queue()
# my_thread = threading.Thread(target=myThread, args=(queue,))
# my_thread.start()
#
# while True:
#     try:
#         exception = queue.get()
#     except queue.empty():
#         pass
#     else:
#         print(exception)
#         break


# queue = queue.Queue()
# queue.put(1)
# queue.get(False)


# import multiprocessing
#
#
# class MyProcess(multiprocessing.Process):
#     def __init__(self):
#         super(MyProcess, self).__init__()
#
#     def run(self):
#         print("Child Process PID: {}".format(multiprocessing.current_process().pid))
#
#
# def main():
#     print("Main Process PID: {}".format(multiprocessing.current_process().pid))
#     myProcess = MyProcess()
#     myProcess.start()
#     myProcess.join()
#
#
# if __name__ == "__main__":
#     main()

from multiprocessing import Pool

def task(n):
    print(n)

def main():
    with Pool(4) as p:
        print(p.map(task, [2,3,4]))

import experiment49

if __name__ == "__main__":
    main()



