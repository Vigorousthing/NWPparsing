import matplotlib.pyplot as plt
import sys


class Visualizer:
    def __init__(self):
        pass

    @staticmethod
    def correlation_matrix(df, col_name_list):
        corr_df = df[col_name_list].corr()
        plt.matshow(corr_df)
        plt.xticks(range(len(corr_df.columns)), corr_df.columns)
        plt.yticks(range(len(corr_df.columns)), corr_df.columns)
        plt.colorbar()
        plt.show()

        corr_with_real = corr_df["real"]
        print(corr_with_real)
        return corr_with_real

    @staticmethod
    def print_progress(iteration, total, prefix='', suffix='',
                       decimals=1, barLength=100):
        format_str = "{0:." + str(decimals) + "f}"
        percent = format_str.format(100 * (iteration / float(total)))
        filled_length = int(round(barLength * iteration / float(total)))
        bar = '#' * filled_length + '-' * (barLength - filled_length)
        sys.stdout.write(
            '\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()

    @staticmethod
    def plot_some_points(*points_lists, marker_size=1):
        # print(points_lists[0])
        # print(points_lists[1])

        color_list = ["red", "blue", "green", "yellow"]
        for i_1, val_first in enumerate(points_lists):
            points_list = val_first
            for i_2, val_second in enumerate(points_list):
                plt.plot(points_list[i_2][1], points_list[i_2][0],
                         "ro", color=color_list[i_1],
                         markersize=marker_size + i_1)
        # plt.plot(lon_given, lat_given, "ro", color="blue")
        plt.grid(True)
        plt.show()
