*****
Stock Extractor
*****

This package includes a series of stock data extractor class from a few widely used sources, such as Yahoo Finance,
Barchart.com, etc.


=====
Installation
=====

``pip install stock_extractor``

The package has the following dependencies:

	* requests
	* pandas
	* beautifulsoup4


=====
USAGE
=====

The package currently has four extractor class

	* SP500Extractor

	  It is used to extract stock data about S&P 500 companies

	* YahooFinanceInfoExtractor

	  It is used to extract latest stock data and information from Yahoo Finance

	* YahooFinanceHistoryQuoteExtractor

	  It is used to extract historical quote data for stocks from Yahoo Finance

	* YahooFinanceDivExtractor

	  It is used to extract historical dividend data for stocks from Yahoo Finance

SP500Extractor
-----

.. code-block:: python

	# import extractor class
	from stock_extractor import SP500Extractor

	extractor = SP500Extractor()

	# get_sp500_symbol_list() returns all SP500 company symbols as a list
	sp500_symbols = extractor.get_sp500_symbol_list()

	# get_sp500_data_by_type(type) retrieves sp500 company stock infomation and store the result in a pandas dataframe
	# type can be 'main', 'technical', or 'performance'
	# 'main' includes fields: 'Symbol', 'Name', 'Last Price', 'Change', 'Percent', 'High', 'Low', 'Volume', 'Time'
	# 'technical' includes fields: 'Symbol', 'Name', 'Last Price', 'Opinion', '20D-Strength', '20D-Volty', '20D-AVol', '52W-Low', '52W-High'
	# 'performance' includes fields: 'Symbol', 'Name', 'Last Price', 'Weighted-Alpha', 'YTD-Pct', '1Month-Pct Change', '3Month-Pct Change', '1Year-Pct Change'
	extractor.get_sp500_data_by_type('technical')

	# get_sp500_full_data() will retrieve all three types of data and combine them into the dataframe
	extractor.get_sp500_full_data()

	# get_dataframe() will return the dataframe that stores retrieved data
	extractor.get_dataframe()

	# save_to_csv(filepath) will save the dataframe as a csv file
	extractor.save_to_csv('sp500_data.csv')


YahooFinanceInfoExtractor
-----

This extractor class extract latest stock data and stock information on Yahoo Finance
The fields that can be extracted from this class include:

'Ask', 'AvgDVol', 'AskSize', 'Bid', 'AskRealTime', 'BidRealTime', 'BookValue', 'BidSize', 'Change&Pct', 'Change',
'Commission', 'ChangeRealTime', 'AfterHourChangeRealTime', 'Dividend', 'LastTradeDate', 'TradeDate', 'EPS',
'ErrorIndication', 'EPSE_CurrentYear', 'EPSE_NextYear', 'EPSE_NextQuarter', 'FloatShares', 'D-Low', 'D-High',
'52W-Low', '52W-High', 'HoldingsGainPercent', 'AnnualizedGain', 'HoldingsGain', 'HoldingsGainPercentRealTime',
'HoldingsGainRealTime', 'MoreInfo', 'OrderBookRealTime', 'MarketCap', 'MarketCapRealTime', 'EBITDA',
'ChangeFrom52W-Low', 'PctChangeFrom52W-Low', 'LastTradeRealTime', 'PctChangeRealTime', 'LastTradeSize',
'ChangeFrom52W-High', 'PctChangeFrom52W-High', 'LastTradeWithTime', 'LastTradePrice', 'HighLimit',
'LowLimit', 'DayRange', 'DayRangeRealTime', '50MA', '200MA', 'ChangeFrom200MA', 'PctChangeFrom200MA',
'ChangeFrom50MA', 'PctChangeFrom50MA', 'Name', 'Notes', 'Open', 'PreviousClose', 'PricedPaid', 'PctChange',
'Price/Sales', 'Price/Book', 'Ex-DividendDate', 'P/E', 'DividendPayDate', 'P/E_RealTime', 'PEG',
'P/E-EstCurrentYear', 'P/E-EstNextYear', 'Symbol', 'SharesOwned', 'ShortRatio', 'LastTradeTime', 'TradeLinks',
'TickerTrend', '1YrTarget', 'Volume', 'HoldingsValue', 'HoldingsValueRealTime', '52W-Range', 'DayValueChange',
'DayValueChangeRealTime', 'StockExchange', 'Yield'

Example:

.. code-block:: python

	# import extractor class
	from stock_extractor import YahooFinanceInfoExtractor

	extractor = YahooFinanceInfoExtractor()

	# read a list of symbols from txt file.
	# extractor.set_symbol_list(symbol_list) can set symbol list as python list
	extractor.read_symbol_list_from_txt('../sample_data/sample_symbol_list.txt')

	# set which fields are included in extraction
	extractor.set_field_list([
		'Symbol', 'LastTradePrice', 'LastTradeDate', 'LastTradeTime', 'D-High', 'D-Low', '52W-High', '52W-Low',
		'50MA', '200MA', 'PctChangeFrom50MA', 'PctChangeFrom200MA', 'EBITDA', 'MarketCap',
		'Dividend', 'Yield', 'EPS', 'P/E', 'PEG', 'Price/Sales', 'Price/Book', 'Name'
	])

	# extract data from Yahoo Finance
	extractor.load_yahoo_data()

	# save the result in a csv file
	# you can call extractor.get_dataframe() to return the result as pandas dataframe
	extractor.save_to_csv('../output/sample_stock_info.csv')

YahooFinanceHistoryQuoteExtractor
-----

This extractor extract historical quote data for the input symbol list for a time span

Example:

.. code-block:: python

	# import extractor class
	from stock_extractor import YahooFinanceHistoryQuoteExtractor

	extractor = YahooFinanceHistoryQuoteExtractor()

	# set start and end date for extraction
	extractor.set_end_date('2016-01-01')
	extractor.set_start_date('2015-01-01')

	# set symbol list, you can also set this from a txt file, see example above
	extractor.set_symbol_list(['CAT', 'SPLS', 'ETP', 'HCP', 'T'])

	# the method that actually extracts data from Yahoo Finance
	extractor.load_data_by_symbol_list()

	# filter out other fields, leave only adj price here since this field is usually what people need.
	extractor.get_adj_price_only_dataframe()

	#return the result as a pandas dataframe
	extractor.get_dataframe()

	# save the result as csv file
	extractor.save_to_csv()

YahooFinanceDivExtractor
-----

This extractor extracts historical dividend data from Yahoo Finance.
The api is very similar to the previous one.

Example:

.. code-block:: python

	# import extractor class
	from stock_extractor import YahooFinanceDivExtractor

	extractor = YahooFinanceDivExtractor()
	extractor.set_end_date('2016-01-01')
	extractor.set_start_date('2001-01-01')
	extractor.read_symbol_list_from_txt('../sample_data/sample_symbol_list.txt')
	extractor.load_data_by_symbol_list()
	extractor.get_dataframe()
	extractor.save_to_csv()

TEST
=====

run this code

``$ python -m unittest discover``


CONTACT
=====

The package is created by Zach Liu. Please send email to zachliugis@gmail.com if you have questions or comments.

LICENCE
=====

MIT

