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

    @staticmethod
    def print_progress(iteration, total, prefix='', suffix='',
                       decimals=1, barLength=100):
        format_str = "{0:." + str(decimals) + "f}"
        percent = format_str.format(100 * (iteration / float(total)))
        filled_length = int(round(barLength * iteration / float(total)))
        bar = '#' * filled_length + '-' * (barLength - filled_length)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()
