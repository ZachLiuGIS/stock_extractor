from stock_extractor import (
    YahooFinanceInfoExtractor, YahooFinanceHistoryQuoteExtractor, YahooFinanceDivExtractor
)


if __name__ == '__main__':
    choice = 5
    if choice == 1:
        extractor = YahooFinanceInfoExtractor()
        extractor.read_symbol_list_from_txt('../input/my_portfolio.txt')
        extractor.load_yahoo_data()
        extractor.save_to_csv('../output/my_portfolio_info.csv')

    if choice == 2:
        extractor = YahooFinanceHistoryQuoteExtractor()
        extractor.set_end_date('2016-01-01')
        extractor.set_start_date('2015-01-01')
        extractor.set_symbol_list(['CAT', 'SPLS', 'ETP', 'HCP', 'T'])
        extractor.load_data_by_symbol_list()
        extractor.get_adj_price_only_dataframe()
        extractor.get_dataframe()
        extractor.save_to_csv('../output/hist_prices.csv')

    if choice == 3:
        extractor = YahooFinanceHistoryQuoteExtractor()
        extractor.set_end_date('2016-01-27')
        extractor.set_start_date('2016-01-01')
        extractor.set_symbol_list(['CAT'])
        extractor.load_data_by_symbol_list()
        extractor.get_dataframe()
        extractor.save_to_csv('../output/cat_hist_prices.csv')

    if choice == 4:
        extractor = YahooFinanceDivExtractor()
        extractor.set_end_date('2016-01-01')
        extractor.set_start_date('2001-01-01')
        extractor.read_symbol_list_from_txt('../input/my_portfolio.txt')
        extractor.load_data_by_symbol_list()
        extractor.get_dataframe()
        extractor.save_to_csv('../output/my_portfolio_dividend_history.csv')

    if choice == 5:
        extractor = YahooFinanceDivExtractor()
        extractor.set_end_date('2016-01-01')
        extractor.set_start_date('2001-01-01')
        extractor.set_symbol_list(['ETP'])
        extractor.load_data_by_symbol_list()
        extractor.add_year_and_month_columns_to_dataframe()
        extractor.get_dataframe()
        extractor.save_to_csv('../output/dividend_history_by_year.csv')


