import time
import os
import requests
import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


class BaseExtractor(object):
    class SettingError(Exception):
        pass

    def __init__(self):
        """used to store extract result"""
        self.df = None

    def _get_url_response(self, url, qs):
        success = False
        retry_count = 0
        resp = None

        # try three more times with 5, 25, 125 seconds interval if requests error
        while not success:
            try:
                resp = requests.get(url, qs)
                success = True
            except (requests.HTTPError, requests.ConnectionError) as ex:
                if retry_count < 3:
                    retry_count += 1
                    sleep_period = 5 ** retry_count
                    time.sleep(sleep_period)
                else:
                    raise
        return resp

    def get_dataframe(self):
        """return the dataframe at current state"""
        return self.df

    def save_to_csv(self, filepath='output.csv'):
        """save dataframe to csv"""
        if not filepath[-4:] == '.csv':
            filepath += '.csv'
        self.df.to_csv(filepath, index=True)


class YahooFinanceBaseExtractor(BaseExtractor):
    class SettingError(Exception):
        pass

    def __init__(self):
        super().__init__()
        self.symbol_list = []

    def set_symbol_list(self, symbol_list):
        self.symbol_list = symbol_list

    def read_symbol_list_from_txt(self, filepath):
        with open(filepath) as f:
            symbols = [symbol.strip() for symbol in f]
            self.symbol_list = symbols

    def get_dataframe(self):
        return self.df

    def save_to_csv(self, filepath='yahoo_data_download.csv'):
        if not filepath[-4:] == '.csv':
            filepath += '.csv'
        self.df.to_csv(filepath, index=True)


class YahooFinanceHistoryBaseExtractor(YahooFinanceBaseExtractor):

    def __init__(self):
        super().__init__()
        self.stock_hist_url = r'http://ichart.yahoo.com/table.csv'
        self.end_date = date.today()
        self.start_date = self.end_date + relativedelta(months=-1)

    def set_start_date(self, date_str):
        """Set the start date
        """
        self.start_date = parse(date_str).date()

        # there's no data for the future, so the latest end date is today
        if self.start_date > self.end_date:
            raise self.SettingError('start_date cannot be set to date after end_date')

    def set_end_date(self, date_str):
        """Set the end date
        """
        self.end_date = parse(date_str).date()

        # there's no data for the future, so the latest end date is today
        if self.end_date > date.today():
            self.end_date = date.today()

    def set_date_range(self, start_date, end_date=None):
        """set start and end date"""
        if end_date:
            self.set_end_date(end_date)
        self.set_start_date(start_date)

    def get_url_response(self, url, qs):
        resp = requests.get(url, qs)
        resp.raise_for_status()
        return resp

    def get_query_string(self, symbol):
        """set query stirng for query url"""
        qs = {}
        start_date = self.start_date
        end_date = self.end_date
        qs['c'] = start_date.year
        qs['a'] = start_date.month - 1
        qs['b'] = start_date.day
        qs['f'] = end_date.year
        qs['d'] = end_date.month - 1
        qs['e'] = end_date.day
        qs['s'] = symbol
        return qs

    def load_data_by_symbol(self, symbol):
        raise NotImplementedError('`load_data_by_symbol(symbol)` must be implemented.')

    def load_data_by_symbol_list(self):
        """load historical prices for the list of symbols"""
        df_list = []
        for symbol in self.symbol_list:
            df = self.load_data_by_symbol(symbol)
            df_list.append(df)
        self.df = pd.concat(df_list, axis=1)
