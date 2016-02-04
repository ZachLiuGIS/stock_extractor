from stock_extractor import SP500Extractor


def run_demo(choice):
    if choice == 1:
        extractor = SP500Extractor()
        sp500_symbols = extractor.get_sp500_symbol_list()
        print(sp500_symbols)
        print(len(sp500_symbols))

    if choice == 2:
        extractor = SP500Extractor()
        extractor.get_sp500_data_by_type('technical')
        print(extractor.get_dataframe().info())

    if choice == 3:
        extractor = SP500Extractor()
        extractor.get_sp500_data_by_type('technical')
        print(extractor.get_dataframe().info())

    if choice == 4:
        extractor = SP500Extractor()
        extractor.get_sp500_data_by_type('performance')
        print(extractor.get_dataframe().info())

    if choice == 5:
        extractor = SP500Extractor()
        extractor.get_sp500_full_data()
        extractor.save_to_csv(r'../output/sp500_data.csv')


if __name__ == '__main__':
    run_demo(1)






