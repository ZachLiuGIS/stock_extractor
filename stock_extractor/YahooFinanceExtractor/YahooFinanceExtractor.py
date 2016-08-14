from io import StringIO
import requests
import pandas as pd
from stock_extractor.BaseExtractor.BaseExtractor import YahooFinanceBaseExtractor, YahooFinanceHistoryBaseExtractor
from .constants import yahoo_tag_lookup


#  YahooFinance class to extract finance data
class YahooFinanceInfoExtractor(YahooFinanceBaseExtractor):

    def __init__(self):
        super().__init__()
        self.stock_info_url = r'http://download.finance.yahoo.com/d/quotes.csv'
        self.field_list = ['Symbol', 'LastTradePrice', 'LastTradeDate', 'LastTradeTime', 'D-High', 'D-Low',
                           'Dividend', 'Yield', 'P/E', 'Price/Sales', 'Price/Book', 'Name']

    def set_field_list(self, field_list):
        self.field_list = field_list

    def get_tag_param(self):
        str_list = []
        for field in self.field_list:
            str_list.append(yahoo_tag_lookup.get(field, ''))
        return ''.join(str_list)

    def get_symbol_param(self):
        return '+'.join(self.symbol_list)

    def load_yahoo_data(self):
        params = {
            's': self.get_symbol_param(),
            'f': self.get_tag_param()
        }
        resp = requests.get(self.stock_info_url, params)
        resp.raise_for_status()
        self.df = pd.read_csv(StringIO(resp.content.decode('utf-8')), header=None, names=self.field_list)

    def get_stock_info(self, symbol):
        self.set_field_list([
            'Symbol', 'LastTradePrice', 'LastTradeDate', 'LastTradeTime', 'D-High', 'D-Low', '52W-High', '52W-Low',
            '50MA', '200MA', 'PctChangeFrom50MA', 'PctChangeFrom200MA', 'EBITDA', 'MarketCap',
            'Dividend', 'Yield', 'EPS', 'P/E', 'PEG', 'Price/Sales', 'Price/Book', 'Name'
        ])
        self.set_symbol(symbol)
        self.load_yahoo_data()
        df = self.get_dataframe()
        return {x: y[0] for (x, y) in df.to_dict().items()}


class YahooFinanceHistoryQuoteExtractor(YahooFinanceHistoryBaseExtractor):

    def __init__(self):
        super().__init__()

    def get_query_string(self, symbol):
        """set query stirng for query url"""
        qs = super().get_query_string(symbol)
        qs['g'] = 'd'
        return qs

    def load_data_by_symbol(self, symbol):
        """load full history data for a symbol"""
        qs = self.get_query_string(symbol)
        resp = self.get_url_response(self.stock_hist_url, qs)
        df = pd.read_csv(StringIO(resp.content.decode('utf-8')), parse_dates=['Date'])

        # rename columns to avoid name conflicts when concat
        df.columns = [column + '_' + symbol if column != 'Date' else 'Date' for column in df.columns]
        df.rename(columns={'Adj Close_' + symbol: symbol}, inplace=True)
        df.set_index('Date', inplace=True)
        return df

    def get_adj_price_only_dataframe(self):
        self.df = self.df[self.symbol_list]


class YahooFinanceDivExtractor(YahooFinanceHistoryBaseExtractor):

    def __init__(self):
        super().__init__()

    def get_query_string(self, symbol):
        """set query stirng for query url"""
        qs = super().get_query_string(symbol)
        qs['g'] = 'v'
        return qs

    def load_data_by_symbol(self, symbol):
        """load full history data for a symbol"""
        qs = self.get_query_string(symbol)
        resp = self.get_url_response(self.stock_hist_url, qs)
        df = pd.read_csv(StringIO(resp.content.decode('utf-8')), parse_dates=['Date'])

        # rename columns to avoid name conflicts when concat
        df.columns = [symbol if column != 'Date' else 'Date' for column in df.columns]
        df.set_index('Date', inplace=True)
        return df

    def add_year_and_month_columns_to_dataframe(self):
        self.df['Year'] = self.df.index.map(lambda x: x.year)
        self.df['Month'] = self.df.index.map(lambda x: x.month)