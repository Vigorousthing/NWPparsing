import pandas as pd
import numpy as np

df = pd.DataFrame(np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3], [1, 2, 3]]), columns=["a", "b", "c"])

srs = pd.Series([5,6,7,8])

# print srs
# print df
df["new"] = srs

# print df

# df2 = pd.DataFrame(np.array([[5, 6, 7, 1], [11, 25, 32, 9], [9, 2, 4, 33], [1, 4, 3, 22]]), columns=["a", "b", "c", "new"])

df2 = pd.DataFrame(index=range(4))
df2["a"] = [1,2,3, 4]
df2["b"] = [4,5,6, 4]
df2["c"] = [11, 3, 6, 5]
df2["new"] = [99, 8, 3, 7]

# print df2


df = df.append(df2)
# print df

df3 = pd.DataFrame(np.array([1,2,3,4]), columns=["fcst_tm"])
df3["crtn_tm"] = "22"
# print df3

df4 = pd.DataFrame(index=range(4))
df4["323"] = "22"
# print df4

print(df2)

df5 = pd.DataFrame(columns=["a", "b", "c", "new"])

df5 = df5.append(df2)

print(df5)