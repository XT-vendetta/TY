# -*- coding: utf-8 -*
import datetime
import os
import time

from WindPy import w
from pandas import DataFrame
from pandas import Series
from pandas.tseries.offsets import *

MARKET_DATA_DIR = 'D:/marketdata/SH'
LOAD_MARKET_DATA_LOG = 'D:/marketdata/log.txt'
INDICATORS = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'AMT', 'DEALNUM', 'ADJFACTOR', 'TURN']

'''
万德历史数据
指标名称        指标代码

前收盘价       PRE_CLOSE
开盘价         OPEN
最高价         HIGH
最低价         LOW
收盘价         CLOSE
均价           VWAP
成交量         VOLUME
成交额         AMT
成交笔数       DEALNUM
振幅           SWING
涨跌           CHANGE
涨跌幅(%)      PCT_CHG
换手率(%)      TURN
'''


def load_stock_codes(index_code):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    file_path = os.path.join(data_dir, index_code + '.txt')
    df = DataFrame.from_csv(file_path)
    stock_codes = df['wind_code'].tolist()
    return stock_codes


def load_all_stock_codes():
    retval = []
    indices = ['000001.SH', '399106.SZ']
    for index in indices:
        retval += load_stock_codes(index)
    return retval


def wind_data_to_dataframe(wind_data, index_type='Times'):
    fields = wind_data.Fields
    if index_type == 'Times':
        index = wind_data.Times
    elif index_type == 'Codes':
        index = wind_data.Codes
    data = wind_data.Data
    stock_dict = dict()
    i = 0
    for field in fields:
        stock_dict[field] = data[i]
        i += 1
    df = DataFrame(stock_dict, index=index)
    return df


def wind_get_index_constituent(index_code='000001.SH', indicators=['wind_code', 'i_weight'], date=None, auto_save=True):
    w.start()
    query_date = date if date is not None else datetime.datetime.today()
    query_date_string = query_date.strftime('%Y%m%d')
    query_arg = 'date=' + query_date_string + ';'
    query_arg += 'windcode=' + index_code + ';'
    query_arg += 'field=' + ','.join(indicators)
    index_constituent = w.wset("IndexConstituent", query_arg)
    w.close()
    df = wind_data_to_dataframe(index_constituent, 'Codes')
    if auto_save:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        df.to_csv(os.path.join(data_dir, index_code + '.txt'), sep=',', columns=indicators)
    return df


'''
total_shares
free_float_shares
eps_ttm
eps_basic
eps_diluted
bps             每股净资产

west_eps        预测每股收益
west_stdeps
west_medianeps
west_maxeps
west_mineps
    option: e.g. year=2017;tradeDate=20170605;westPeriod=180

'''


def wind_get_stock_fundamental_data(stock_ids=None, in_indicators=None, date=None, auto_save=True):
    query_date = date if date is not None else datetime.datetime.today()
    query_date_string = query_date.strftime('%Y%m%d')
    indicators = in_indicators if in_indicators is not None else ['TOTAL_SHARES', 'FREE_FLOAT_SHARES', 'EPS_TTM', 'BPS']
    options = 'rptDate=' + query_date_string + ';'
    options += 'currencyType=;'

    w.start()
    data = w.wss(stock_ids, indicators, options)
    df = wind_data_to_dataframe(data, 'Codes')
    today = datetime.datetime.today()
    this_year = today.year
    for y in range(this_year, this_year + 3):
        last_business_day = today - BDay(1)
        options = 'year=' + str(y) + ';tradeDate=' + last_business_day.strftime('%Y%m%d') + ';westPeriod=180'
        west_eps = w.wss(stock_ids, 'WEST_EPS', options)
        indicator = 'WEST_EPS_' + str(y)
        indicators.append(indicator)
        df[indicator] = Series(west_eps.Data[0], index=df.index)
    w.close()
    if auto_save:
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        df.to_csv(os.path.join(data_dir, 'fundamental.csv'), sep=',', columns=indicators)
    return df


def wind_get_stock_historical_market_data(stock_ids=None, indicators=INDICATORS, start_date=None, end_date=None):
    w.start()
    if stock_ids is None:
        stock_ids = load_stock_codes()
    log_file = open(LOAD_MARKET_DATA_LOG, 'w')
    for stock_id in stock_ids:
        try:
            time_start = time.time()
            file_name = os.path.join(MARKET_DATA_DIR, stock_id + '.csv')
            last_line = None
            # If the file exist append the new market data
            if os.path.isfile(file_name):
                need_header = False
                df_old = DataFrame.from_csv(file_name)
                old_date_time = df_old.index.tolist()[0]
                new_date_time = old_date_time + datetime.timedelta(1)
                new_date_str = new_date_time.strftime('%Y-%m-%d')
                if new_date_time > datetime.datetime.today():
                    continue
            # default to get one year market data
            else:
                need_header = True
                new_date_str = datetime.datetime.today() - datetime.timedelta(365)

            stock = w.wsd(stock_id, indicators, new_date_str, datetime.datetime.today(), "PriceAdj=F")

            df = wind_data_to_dataframe(stock)
            df.to_csv(file_name, mode='a', sep=',', header=need_header)
            print 'Finish updating market data for ' + stock_id + ', time used ' + str(time.time() - time_start) + '.'

        except Exception, e:
            log_file.write('Error updating market data for ' + stock_id + '.' + e.message)
    log_file.close()
    w.stop()
