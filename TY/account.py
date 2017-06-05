from TY.utility.trading_date import *
from TY.utility.static_data import *


class StockPosition:
    def __init__(self, trade_date, num_stock, price):
        self.trade_date = trade_date
        self.num_stock = num_stock
        self.price = price


class TradingCost:
    def __init__(self, commission_rate=0.0005, min_commission=5, tax_rate=0.001):
        self.commission_rate = commission_rate
        self.min_commission = min_commission
        self.tax_rate = tax_rate


class Account:
    def __init__(self, cash, date):
        self.date = date
        self.next_date = next_trading_date(self.date)
        self.cash = cash
        self.stocks = dict()
        self.balance = cash
        self.trading_cost = TradingCost()

    def advance_date(self):
        self.date = self.next_date
        self.next_date = next_trading_date(self.next_date)

    def apply_strategy(self, strategy):
        pass

    def update_balance(self, balance_date=None):
        balance = 0
        for stock_id, stock_positions in self.stocks.items():
            position = 0
            for stock_position in stock_positions:
                position += stock_position.num_stock
            balance += position * static_stock_data[stock_id].get_value(
                self.next_date if balance_date is None else balance_date, 'CLOSE')
        balance += self.cash
        self.balance = balance

    def buy(self, stock_id, num_stock, price):
        assert num_stock > 0, 'Number of stock should be larger then zero: ' + stock_id + ' num_stock = ' + num_stock + '.'
        commission = max(num_stock * price * self.trading_cost.commission_rate, 5)
        buy_cost = num_stock * price + commission
        assert buy_cost < self.cash, 'Not enough cash to buy stock: ' + stock_id + ' at price: ' + price + '.'
        if stock_id in self.stocks.keys():
            self.stocks[stock_id].append(StockPosition(self.next_date, num_stock, price))
        else:
            self.stocks[stock_id] = [StockPosition(self.next_date, num_stock, price)]
        self.cash -= buy_cost
        self.update_balance()

    def sell(self, stock_id, num_stock, price):
        assert num_stock > 0, 'Number of stock should be larger then zero: ' + stock_id + ' num_stock = ' + num_stock + '.'
        assert stock_id in self.stocks.keys(), 'Cannot sell stock: ' + stock_id + ', do not have in position.'
        position = 0
        for stock_position in self.stocks[stock_id]:
            position += stock_position.num_stock
        assert num_stock <= position, 'Cannot sell ' + num_stock + ' of stock :' + stock_id + ', only ' + position + ' in position.'
        if num_stock == position:
            self.stocks.pop(stock_id)
        else:
            self.stocks[stock_id].append(StockPosition(self.next_date, -num_stock, price))
        commission = max(num_stock * price * self.trading_cost.commission_rate, 5)
        self.cash += (num_stock * price * (1 - self.trading_cost.tax_rate) - commission)
        self.update_balance()