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
    reordered_list = column_values.to_list()
    reordered_list.reverse()

    candles_list = []
    for i in range(0, len(reordered_list) -1):
        candles_list.append(reordered_list[i + 1] - reordered_list[i])
    logger.debug("list_to_use is [ " + ', '.join(str(x) for x in reordered_list) + ' ]')
    logger.debug("candles_list is [ " + ', '.join(str(x) for x in candles_list) + ' ]')

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

def is_day_candle_better_over_avg_and_mode(last_five_candles_up_list):
    """
    For all element in the list, if element > average or mode then the score is 1, otherwise 0

    :param last_five_candles_up_list: a list of last 5 candles up per day
    :return: 2 lists of 0 & 1 values, 1 meaning the last 5 candles are above the average or the mode, 0 otherwise
    """
    versus_mode_list = last_five_candles_up_list[:]

    # average
    average = statistics.mean(last_five_candles_up_list)
    logger.debug("Average of the list of 5 candles up per day is " + str(average) )

    last_five_candles_up_list[:] = [ 1 if i > average else 0 for i in last_five_candles_up_list ]
    logger.info("list of 0 & 1 values is versus avergage : [ " + ', '.join( str(x) for x in last_five_candles_up_list ) + ' ]')

    #mode
    mode = statistics.mode(versus_mode_list)
    logger.debug("Mode of the list of 5 candles up per day is " + str(mode))
    versus_mode_list[:] = [ 1 if i > mode else 0 for i in versus_mode_list ]
    logger.info("list of 0 & 1 values versus mode is : [ " + ', '.join( str(x) for x in versus_mode_list ) + ' ]')


    return last_five_candles_up_list, versus_mode_list


if __name__ == '__main__':
    ''' first arg is the fileName, ex : "resources/eth_csv.csv"
        second arg is the column name to get data from, ex : 'close'
    '''
    file_name = os.path.abspath(str(sys.argv[1]))
    file_name = file_name.replace('\\', '/')
    column_name = str(sys.argv[2])

    values = full_values_from_one_column(file_name, column_name)
    candles_up = build_up_csv_for_filter(values)

    #generating the csv file versus mean
    day_candle_vs_average_list, day_candle_vs_mode_list = is_day_candle_better_over_avg_and_mode(candles_up)

    logger.info("Creating resources/token.csv file with day_candle_vs_average_list")
    df = pd.DataFrame(day_candle_vs_average_list, columns=["token"])
    df.to_csv('resources/token_versus_mean.csv', index=False)

    # generating the csv file versus mode
    logger.info("Creating resources/token.csv file with day_candle_vs_mode_list")
    df = pd.DataFrame(day_candle_vs_mode_list, columns=["token"])
    df.to_csv('resources/token_versus_mode.csv', index=False)