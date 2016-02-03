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

The package currently has only one extractor class - SP500Extractor
It is used to extract stock data about S&P 500 companies

SP500Extractor
-----

::
	# import extractor class
	from stock_extractor.BarchartExtractor.sp_500_extract import SP500Extractor

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

TEST
=====
run ::
	python -m unittest discover


CONTACT
=====

The package is created by Zach Liu. Please send email to zachliugis@gmail.com if you have questions or comments.

LICENCE
=====

MIT

