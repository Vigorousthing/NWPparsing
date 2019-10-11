import time
import pygrib
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession

conf = SparkConf()
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

pygrib_read_time = time.time()


def read_file_from_hdfs(rdd):
    file = pygrib.fromstring(rdd[1])
    maxt = file.values
    return maxt.shape[0], maxt.shape[1], maxt.min().item(), maxt.max().item()


files = sc.binaryFiles("hdfs://10.0.1.36:9000/test/ldaps_test/")
df = files.map(read_file_from_hdfs).map(lambda x: (x,)).toDF()
df.show(truncate=False)

print("--- %s seconds(pygrib_read_time) ---" % (time.time() - pygrib_read_time))

sc.stop()
