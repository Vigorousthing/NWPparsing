import unittest
from util.input_converter import *


class MyTest(unittest.TestCase):
    def test_one_plus_two(self):
        InputConverter().time_interval_from_m_w()
        self.assertEqual(1+2, 3, "right")

    def test_subtract(self):
        self.assertEqual(1-2, -1)


if __name__ == '__main__':
    unittest.main()
    pass



# import os
# import CONSTANT
# import pandas as pd
#
#
# a = os.listdir(CONSTANT.data_file_path)
# print(a)
#
