# from pyspark import SparkContext, SparkConf
# from pyspark.sql import SparkSession
# import pygrib

# root_path = "hdfs://10.0.3.36:9000/home/keti/Downloads/nwpcorr.png"
# root_path = "hdfs://10.0.3.36:9000/nwp/"
#
# def hihi(path):
#     nwp_file = pygrib.open("hdfs://10.0.3.36:9000/nwp/"+path)
#     value = nwp_file[3].values
#     value = value[155][120]
#     return value
#
# conf = SparkConf().setAppName("app_name").setMaster("local[*]")
# sc = SparkContext(conf=conf)
# spark = SparkSession(sc)
# sc.setSystemProperty("HADOOP_USER_NAME", "keti")
#
# filenames = sc.textFile("hdfs://10.0.3.36:9000/nwp/filenamefile.txt")
#
# filewhat = sc.textFile("hdfs://10.0.4.36:9000/Downloads/example_hadoop.txt")
#
# print(filenames.collect())
# print(filewhat.collect())

# hi = sc.binaryFiles("hdfs://10.0.3.36/nwp")
# result = filenames.map(hihi, filenames)
# result.take(10)


import queue

a = queue.Queue()

a.put(1)
a.put(2)
a.put(3)



