import os
from TY.utility.utility_functions import *
from TY.market_data.wind_data import *

# load trading dates
trading_date_file_dir = os.path.join(os.path.dirname(__file__), 'trading_date.txt')
static_trading_dates = [int(x) for x in read_file_to_list(trading_date_file_dir)]

# load stock ids
sh_stock_ids = load_stock_codes('000001.SH')
sz_stock_ids = load_stock_codes('399106.SZ')
zxb_stock_ids = load_stock_codes('399101.SZ')
cyb_stock_ids = load_stock_codes('399102.SZ')

# load stock data
static_stock_data = dict()
wind_add_new_column(sh_stock_ids, ['PRE_CLOSE'])