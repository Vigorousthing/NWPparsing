from __future__ import print_function
import sys
import time
length_of_loop = 200000

# num = 0
# for i in range(length_of_loop):
#     if i % length_of_loop/20 == 0:
#         print("=", end="")
#         print(str(num/20)+"percent", end="\r")
#         num += 1
#         # sys.stdout.write("rrr")
#         # sys.stdout.flush()

# n = 1000
# for i in range(n):
#     time.sleep(1)
#     print("i:",i,sep='',end="\n")


# for i in xrange(10, 0, -1):
#     sys.stdout.write("\r")
#     sys.stdout.write("{:2d} seconds remaining.".format(i))
#
#     sys.stdout.write("\n")
#     sys.stdout.write("=")
#
#     time.sleep(1)

# def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
#     formatStr = "{0:." + str(decimals) + "f}"
#     percent = formatStr.format(100 * (iteration / float(total)))
#     filledLength = int(round(barLength * iteration / float(total)))
#     bar = '#' * filledLength + '-' * (barLength - filledLength)
#     sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
#     if iteration == total:
#         sys.stdout.write('\n')
#         sys.stdout.flush()
#
# for i in range(0, 100):
#     time.sleep(1)
#     printProgress(i, 100, 'Progress:', 'Complete', 1, 50)

import pandas as pd

col = ["a", "b", "c"]
a = pd.DataFrame(columns=col)

row = pd.Series([12,23,34], index=col)

a.append(row, ignore_index=True)

print(a)