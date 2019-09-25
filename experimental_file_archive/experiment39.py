# file = open("/home/jhpark/experiment_files/cote.txt", "r")
# file = file.read()
# file = file.split("\n")
#
# print(file)

# from concurrent.futures import ThreadPoolExecutor
#
# def task(n):
#     print("processing {}".format(n))
#
# def taskDone(fn):
#     if fn.cancelled():
#         print("our {} future has been cancelled".format(fn.arg))
#     elif fn.done():
#         print("our task has completed")
#
# def secondTaskDone(fn):
#     print("I didn't think this would work")
#
# def main():
#     print("starting threadppolexecutor")
#     with ThreadPoolExecutor(max_workers=3) as executor:
#         future = executor.submit(task, (2))
#         future.add_done_callback(taskDone)
#         future.add_done_callback(secondTaskDone)
#     print("all task complete")
#
# main()

from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
import random

def isEven(n):
    print("checking if {} is even".format(n))
    if type(n) != int:
        raise Exception("Value entered is not an integer")
    if n % 2 == 0:
        print("{} is even".format(n))
        return True
    else:
        print("{} is odd".format(n))
        return False

def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        task1 = executor.submit(isEven, (2))
        task2 = executor.submit(isEven, ("t"))
        task3 = executor.submit(isEven, (3))

    for future in concurrent.futures.as_completed([task1, task2, task3]):
        print("result of task: {}".format(future.result()))

main()