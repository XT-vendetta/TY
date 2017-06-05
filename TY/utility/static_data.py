import os
from TY.utility.utility_functions import *


# load trading dates
trading_date_file_dir = os.path.join(os.path.dirname(__file__), 'trading_date.txt')
static_trading_dates = [int(x) for x in read_file_to_list(trading_date_file_dir)]

# load stock ids
sh_stock_codes_file_dir = os.path.join(os.path.dirname(__file__), '../market_data/data/SH_stock_codes.txt')
sz_stock_codes_file_dir = os.path.join(os.path.dirname(__file__), '../market_data/data/SZ_stock_codes.txt')
zxb_stock_codes_file_dir = os.path.join(os.path.dirname(__file__), '../market_data/data/ZXB_stock_codes.txt')
cyb_stock_codes_file_dir = os.path.join(os.path.dirname(__file__), '../market_data/data/CYB_stock_codes.txt')

sh_stock_ids = read_file_to_list(sh_stock_codes_file_dir)
sz_stock_ids = read_file_to_list(sz_stock_codes_file_dir)
zxb_stock_ids = read_file_to_list(zxb_stock_codes_file_dir)
cyb_stock_ids = read_file_to_list(cyb_stock_codes_file_dir)

# load stock data
static_stock_data = dict()