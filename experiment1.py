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

# def our_thread(i):
#     print("thread {} started".format(i))
#     time.sleep(i*2)
#     print("thread {} finished".format(i))
#
#
# thread1 = threading.Thread(target=our_thread, args=(1,))
# thread1.start()
# print("is thread 1 finished?")
#
# thread2 = threading.Thread(target=our_thread, args=(2,))
# thread2.start()
# # thread2.join()
# print("thread 2 is definetely finished")

# counter = 1
# def worker_a():
#     global counter
#     while counter < 1000:
#         counter += 1
#         print("worker a is incrementing counter to {}".format(counter))
#         # sleeptime = random.randint(0, 1)
#         # time.sleep(sleeptime)
#
#
# def worker_b():
#     global counter
#     while counter > -1000:
#         counter -= 1
#         print("worker b is decrementing counter to {}".format(counter))
#         # sleeptime = random.randint(0, 1)
#         # time.sleep(sleeptime)
#
# t0 = time.time()
# thread1 = threading.Thread(target=worker_a)
# thread2 = threading.Thread(target=worker_b)
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# t1 = time.time()
# print("execution time {}".format(t1 - t0))


# counter = 1
# lock = threading.Lock()
#
#
# def worker_a():
#     global counter
#     lock.acquire()
#     try:
#         while counter < 1000:
#             counter += 1
#             print("worker a is incrementing counter to {}".format(counter))
#             # sleeptime = random.randint(0, 1)
#             # time.sleep(sleeptime)
#     finally:
#         lock.release()
#
#
# def worker_b():
#     global counter
#     lock.acquire()
#     try:
#         while counter > -1000:
#             counter -= 1
#             print("worker b is decrementing counter to {}".format(counter))
#             # sleeptime = random.randint(0, 1)
#             # time.sleep(sleeptime)
#     finally:
#         lock.release()
#
#
# t0 = time.time()
# thread1 = threading.Thread(target=worker_a)
# thread2 = threading.Thread(target=worker_b)
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# t1 = time.time()
# print("execution time {}".format(t1 - t0))


# class MyWorker:
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#         self.r_lock = threading.RLock()
#         self.p_lock = threading.Lock()
#
#     def modify_a(self):
#         with self.p_lock:
#
#             # print("modify a : RLock acquired: {}".format(self.r_lock._is_owned()))
#             print("{}".format(self.p_lock))
#             self.a = self.a + 1
#             time.sleep(3)
#
#     def modify_b(self):
#         with self.p_lock:
#             # print("modify b : RLock acquired: {}".format(self.r_lock._is_owned()))
#             print("{}".format(self.p_lock))
#             self.b = self.b + 1
#             time.sleep(3)
#
#     def modify_both(self):
#         with self.p_lock:
#             print("RLock acquired, modifying A and B")
#             print("{}".format(self.p_lock))
#             self.modify_a()
#             self.modify_b()
#             print("{}".format(self.p_lock))
#
# worker_a = MyWorker()
# worker_a.modify_both()


import datetime

current_time = datetime.datetime.now()
print(current_time)
current_time = datetime.datetime.strptime(current_time, "%Y-%m-%d %H")