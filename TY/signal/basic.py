from __future__ import division


def is_limit_up(stock, date):
    pre_close = stock.at[date, 'PRE_CLOSE']
    close = stock.at[date, 'CLOSE']
    limit_price = round(pre_close * 1.1, 2)
    return limit_price == close


def is_limit_down(stock, date):
    pre_close = stock.at[date, 'PRE_CLOSE']
    close = stock.at[date, 'CLOSE']
    limit_price = round(pre_close * 0.9, 2)
    return limit_price == close


def basic_xing_xian(stock, date):
    open_price = stock.at[date, 'OPEN']
    close_price = stock.at[date, 'CLOSE']
    high_price = stock.at[date, 'HIGH']
    low_price = stock.at[date, 'LOW']

    bool1 = 1.01 * close_price > open_price > 0.99 * close_price
    mid = (open_price + close_price) / 2.0
    bool2 = (low_price + 2 * high_price) / 3.0 > mid > (2 * low_price + high_price) / 3.0
    return bool1 and bool2


def basic_diao_xian(stock, date):
    open_price = stock.at[date, 'OPEN']
    close_price = stock.at[date, 'CLOSE']
    high_price = stock.at[date, 'HIGH']
    low_price = stock.at[date, 'LOW']

    mid = (high_price + low_price) / 2.0
    return min(open_price, close_price) > mid
