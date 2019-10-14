import time
import pygrib
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession


def read_file_from_hdfs(rdd):
    file = pygrib.fromstring(rdd[1])

    print("file_types: ", type(file))
    print("file_name: ", file.expand_grid())
    # print(rdd[0])
    # print(file.data())
    # print(len(file.data()))
    print(file.keys())
    # print(file["dataTime"])
    maxt = file.values
    print(type(maxt))
    return


def start():
    pygrib_read_time = time.time()
    conf = SparkConf()
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)
    files = sc.binaryFiles("hdfs://10.0.1.36:9000/test/ldaps_test/")
    df = files.map(read_file_from_hdfs).map(lambda x: (x,)).toDF()
    df.show(truncate=False)

    print("--- %s seconds(pygrib_read_time) ---" % (
                time.time() - pygrib_read_time))
    sc.stop()


if __name__ == '__main__':
    # a = pygrib.open(
    #     "./data_file/sample_nwp_files/l015_v070_erlo_unis_h002.2019042318.gb2")
    start()

