import matplotlib.pyplot as plt
import sys


class Visualizer:
    def __init__(self):
        pass

    def correlation_matrix(self, df, col_name_list):
        corr_df = df[col_name_list].corr()
        plt.matshow(corr_df)
        plt.xticks(range(len(corr_df.columns)), corr_df.columns)
        plt.yticks(range(len(corr_df.columns)), corr_df.columns)
        plt.colorbar()
        plt.show()

    def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100):
        formatStr = "{0:." + str(decimals) + "f}"
        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()