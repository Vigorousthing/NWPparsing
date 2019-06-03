import threading
import time
import random
from multiprocessing import Process

# def standard_thread():
#     print("starting my standard thread")
#     time.sleep(10)
#     print("ending my standard thread")
#
#
# def daemon_thread():
#     while True:
#         print("sending out heartbeat signal")
#         time.sleep(1)
#
#
# st_thread = threading.Thread(target=standard_thread)
# dm_thread = threading.Thread(target=daemon_thread)
# dm_thread.setDaemon(True)
# dm_thread.start()
# st_thread.start()


# def execute_thread(i):
#     print("thread {} started".format(i))
#     sleep_time = random.randint(1, 10)
#     time.sleep(sleep_time)
#     print("thread {} finished executing".format(i))
#
#
# for i in range(10):
#     thread = threading.Thread(target=execute_thread, args=(i,))
#     thread.start()
#     print("active threads:", threading.enumerate())


# def my_thread(i):
#     print("thread {}: started".format(i))
#     time.sleep(random.randint(1, 10))
#     print("thread {}: finished".format(i))
#
#
# for i in range(random.randint(2, 50)):
#     thread = threading.Thread(target=my_thread, args=(i,))
#     thread.start()
#
# time.sleep(4)
# print("total number of active threads: {}".format(threading.active_count()))


# def thread_target():
#     print("current thread: {}".format(threading.current_thread()))
#
#
# threads = []
# for i in range(10):
#     thread = threading.Thread(target=thread_target)
#     thread.start()
#     threads.append(thread)
#
# for thread in threads:
#     thread.join()


# def my_child_thread():
#     print("child thread starting")
#     time.sleep(5)
#     print("current thread ------")
#     print(threading.current_thread())
#     print("---------------------")
#     print("main thread ---------")
#     print(threading.main_thread())
#     print("---------------------")
#     print("child thread ending")
#
# child = threading.Thread(target=my_child_thread)
# child.start()
# child.join()


# def my_thread(i):
#     print("thread {}: started".format(i))
#     time.sleep(random.randint(1, 5))
#     print("thread {}: finished".format(i))
#
#
# for i in range(4):
#     thread = threading.Thread(target=my_thread, args=(i,))
#     thread.start()
# print("Enumerating: {}".format(threading.enumerate()))


# def my_thread():
#     print("thread {} starting".format(threading.currentThread().getName()))
#     time.sleep(10)
#     print("thread {} ending".format(threading.currentThread().getName()))
#
# for i in range(4):
#     thread_name = "thread-" + str(i)
#     thread = threading.Thread(name=thread_name, target=my_thread)
#     thread.start()
# print("{}".format(threading.enumerate()))


# def my_worker():
#     t1 = time.time()
#     print("process started at: {}".format(i))
#     time.sleep(20)
#
# my_process = Process(target=my_worker)
# print("process {}".format(my_process))
# my_process.start()
# print("terminating process...")
# my_process.terminate()
# my_process.join()
# print("process terminated: {}".format(my_process))


# class Philosopher(threading.Thread):
#     def __init__(self, left_fork, right_fork, name):
#         print("our philosopher has sat down at the table")
#         threading.Thread.__init__(self, name=name)
#         self.left_fork = left_fork
#         self.right_fork = right_fork
#
#     def run(self):
#         print("philosopher: {} has started thinking".format(threading.current_thread().getName()))
#         while True:
#             time.sleep(random.randint(1, 5))
#             print("philosopher {} has finished thinking".format(threading.current_thread().getName()))
#             self.left_fork.acquire()
#             time.sleep(random.randint(1, 5))
#             try:
#                 print("philosopher {} has acquired the left fork".format(threading.current_thread().getName()))
#                 self.right_fork.acquire()
#                 try:
#                     print("philosopher {} has attained both forks, currently eating".format(threading.current_thread().getName()))
#                 finally:
#                     self.right_fork.release()
#                     print("philosopher {} has released the right fork".format(threading.current_thread().getName()))
#             finally:
#                 self.left_fork.release()
#                 print("philosopher {} has released the left fork".format(threading.current_thread().getName()))
#
#
# class Fork:
#     def __init__(self, fork_name):
#         self.fork_name = fork_name
#
#     def acquire(self):
#         pass
#
#     def release(self):
#         pass
#
#
# fork1 = Fork(1)
# fork2 = Fork(2)
# fork3 = Fork(3)
# fork4 = Fork(4)
# fork5 = Fork(5)
#
#
# a = Philosopher(fork1, fork2, "Plato")
# a.run()

