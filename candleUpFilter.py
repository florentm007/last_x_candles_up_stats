import sys, os
import pandas as pd


def full_values_from_one_column(csv_file, column):
    """

    :param csv_file: fileName, ex : "resources/eth_csv.csv"
    :param column: the column name to get data from, ex : 'close'
    :return: values from the column
    """
    df = pd.read_csv(csv_file, sep=';')
    saved_column = df[column]

    return saved_column

def build_up_csv_for_filter(column_values):
    """
    Getting the number of the last 5 candles up, not including the current day.
    So the list start at day +5 and ends at last day
    :param column_values: the ROC of candles
    :return:
    """

    candles_list = []
    for i in range(0, len(column_values) -1):
        candles_list.append(column_values[i + 1] - column_values[i])

    last_five_candles_up = []
    for i in range(0, len(candles_list) +1 ):
        counter = 0
        if i >= 5:
            if candles_list[i - 1] > 0:
                counter += 1
            if candles_list[i - 2] > 0:
                counter += 1
            if candles_list[i - 3] > 0:
                counter += 1
            if candles_list[i - 4] > 0:
                counter += 1
            if candles_list[i - 5] > 0:
                counter += 1

            last_five_candles_up.append(counter)

    print(last_five_candles_up)

    return last_five_candles_up


if __name__ == '__main__':
    ''' first arg is the fileName, ex : "resources/eth_csv.csv"
        second arg is the column name to get data from, ex : 'close'
    '''
    file_name = os.path.abspath(str(sys.argv[1]))
    file_name = file_name.replace('\\', '/')
    column_name = str(sys.argv[2])

    values = full_values_from_one_column(file_name, column_name)
    build_up_csv_for_filter(values)