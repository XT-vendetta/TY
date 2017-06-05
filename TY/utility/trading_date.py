from static_data import *
from datetime import datetime, timedelta
import bisect


def date_to_excel_int(date):
    return (date - datetime(1899, 12, 30)).days


def excel_int_to_date(integer):
    return datetime(1899, 12, 30) + timedelta(integer)


def next_trading_date(date):
    excel_date = date_to_excel_int(date)
    i = bisect.bisect_right(static_trading_dates, excel_date)
    if i:
        return static_trading_dates[i]
    raise ValueError('Next trading date not found.')


def previous_trading_date(date):
    excel_date = date_to_excel_int(date)
    i = bisect.bisect_left(static_trading_dates, excel_date)
    if i:
        return static_trading_dates[i-1]
    return ValueError('Previous trading date not found.')


'''
def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
'''