from TY.utility.static_data import *


# Criterion class to filter stock
# If operator is given, the stock is filtered out if operator(stock_value, value) is False
class FundamentalFilter:
    def __init__(self, indicator, value=None, operator=None):
        self.indicator = indicator
        self.value = value
        self.operator = operator

    def evaluate(self, stock_id):
        stock_value = s_fundamental_stock_data.at[stock_id, self.indicator]
        return self.operator(stock_value, self.value)


class Sorter:
    def __init__(self, indicator, is_ascending = True):
        self.indicator = indicator
        self.is_ascending = is_ascending

    def evaluate(self, stocks):
        series = s_fundamental_stock_data[self.indicator]
        series = series[stocks]
        return series.sort_values(ascending=self.is_ascending)


# n is the maximum number of stock remain after filter
class StockPicker:
    def __init__(self, n, criterion_list, sorter):
        self.n = n
        self.criterion_list = criterion_list
        self.sorter = sorter

    def filter(self, stocks):
        after_criterion_filter = []
        for stock in stocks:
            all_good = True
            for criterion in self.criterion_list:
                if not criterion.evaluate(stock):
                    all_good = False
                    break
            if all_good: after_criterion_filter.append(stock)

        # no need to sort
        if len(after_criterion_filter) <= self.n:
            return after_criterion_filter
        # find the best satisfaction based on sort
        else:
            return self.sorter.evaluate(after_criterion_filter).index.values[0:self.n]


