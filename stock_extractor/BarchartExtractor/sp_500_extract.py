import requests
import pandas as pd
import datetime
import time
from bs4 import BeautifulSoup
from stock_extractor.utils.pandas_utils.dataframe_utils import percentage_string_to_number
from stock_extractor.BaseExtractor.BaseExtractor import BaseExtractor


class SP500Extractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.sp500_url = r'http://www.barchart.com/stocks/sp500.php'

    def _get_html_soup(self, url, qs):
        """get html soup from url, query string"""
        html = self._get_url_response(url, qs).text

        # use BeautifulSoup to parse html table
        soup = BeautifulSoup(html)
        return soup

    def extract_data_from_soup(self, soup, columns):
        """extract table data from soup, returns dataframe"""
        data = []
        tbody = soup.find('table', attrs={'id': 'dt1'}).tbody
        rows = tbody.findAll('tr')
        for row in rows:
            cells = row.findAll('td')
            record = [cells[i].text.strip() for i in range(len(columns))]
            data.append(record)

        df = pd.DataFrame(data, columns=columns)
        df.set_index('Symbol', inplace=True)
        df.replace('N/A', 0)
        return df

    def get_sp500_data_by_type(self, type_='main'):
        """get sp500 data and store in dataframe.
        There are three types of data:
        main, technical, and performance
        """
        columns = ['Symbol', 'Name', 'Last']
        qs = {'view': 'main', '_dtp1': 0}
        pct_columns = []  # percentage string columns need to be cleaned up
        if type_ == 'main':
            columns += ['Change', 'Percent', 'High', 'Low', 'Volume', 'Time']
            pct_columns = ['Percent']
        elif type_ == 'technical':
            columns += ['Opinion', '20D-Strength', '20D-Volty', '20D-AVol', '52W-Low', '52W-High']
            qs.update({'view': 'technical'})
            pct_columns = ['20D-Strength', '20D-Volty']
        elif type_ == 'performance':
            columns += ['W-Alpha', 'YTD-Pct', '1M-Pct', '3M-Pct', '1Y-Pct']
            qs.update({'view': 'performance'})
            pct_columns = ['YTD-Pct', '1M-Pct', '3M-Pct', '1Y-Pct']

        soup = self._get_html_soup(self.sp500_url, qs)

        df = self.extract_data_from_soup(soup, columns)

        percentage_string_to_number(df, pct_columns)

        # Add date to df
        df['Date'] = datetime.date.today()

        if self.df is None:
            self.df = df
        else:
            columns_to_use = df.columns.difference(self.df.columns)
            self.df = self.df.join(df[columns_to_use])
        return df

    def get_sp500_full_data(self):
        """get combines three types of data into single dataframe"""
        for view in ['main', 'technical', 'performance']:
            self.get_sp500_data_by_type(view)

    def get_sp500_symbol_list(self):
        """return the list S&P 500 company symbols"""
        if self.df is None:
            self.get_sp500_data_by_type('main')
        return self.df.index.values.tolist()

