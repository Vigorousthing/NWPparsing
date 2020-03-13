import os
import CONSTANT
import pandas as pd


def merge_files_by_horizontally():
    root_path = CONSTANT.data_file_path + "/merge/"
    filename_list = os.listdir(root_path)

    while True:
        filename = filename_list.pop()
        if filename[11] == "s":
            df = pd.read_excel(root_path + filename)
            break

    for filename in filename_list:
        if filename[11] == "s":
            df = df.append(pd.read_excel(root_path + filename))
    return df

# for filename in filename_list:
#     df = pd.read_excel(root_path + filename)
#     print(df)
# df1 = pd.read_excel(root_path + filename_list[0])
# df2 = pd.read_excel(root_path + filename_list[1])
# merged = df1.append(df2)
# print(merged)


df = merge_files_by_horizontally().drop(columns=["Unnamed: 0"])
df.to_excel(CONSTANT.data_file_path + "{}.xlsx".
                    format("seoulgarage_merged_6to12"))

# root_path = CONSTANT.data_file_path + "/merge/"
# filename_list = os.listdir(root_path)
#
# print(filename_list)
#
# print(filename_list[0][11])
# print(filename_list[1][11])
# print(filename_list[2][11])
# print(filename_list[3][11])
# print(filename_list[4][11])
# print(filename_list[5][11])
# print(filename_list[6][11])
# print(filename_list[7][11])
