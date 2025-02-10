import sys, os
import pandas as pd
import statistics
from loguru import logger

# setting up log level
logger.remove()
logger.add(sink=sys.stdout, level="INFO")


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

    logger.debug("last_five_candles_up is [ " + ', '.join( str(x) for x in last_five_candles_up ) + ' ]')

    return last_five_candles_up

def is_day_candle_better_over_avg(last_five_candles_up_list):
    """
    For all element in the list, if element > average then the score is 1, otherwise 0

    :param last_five_candles_up_list: a list of last 5 candles up per day
    :return: a list of 0 & 1 values, 1 meaning the last 5 candles are above the average, 0 otherwise
    """
    average = statistics.mean(last_five_candles_up_list)
    logger.debug("Average of the list of 5 candles up per day is " + str(average) )

    last_five_candles_up_list[:] = [ 1 if i > average else 0 for i in last_five_candles_up_list ]
    logger.info("list of 0 & 1 values is : [ " + ', '.join( str(x) for x in last_five_candles_up_list ) + ' ]')

    return last_five_candles_up_list


if __name__ == '__main__':
    ''' first arg is the fileName, ex : "resources/eth_csv.csv"
        second arg is the column name to get data from, ex : 'close'
    '''
    file_name = os.path.abspath(str(sys.argv[1]))
    file_name = file_name.replace('\\', '/')
    column_name = str(sys.argv[2])

    values = full_values_from_one_column(file_name, column_name)
    candles_up = build_up_csv_for_filter(values)
    day_candle_vs_average_list = is_day_candle_better_over_avg(candles_up)

    #generating the csv file
    logger.info("Creating resources/token.csv file with day_candle_vs_average_list")
    df = pd.DataFrame(day_candle_vs_average_list, columns=["token"])
    df.to_csv('resources/token_versus_mean.csv', index=False)