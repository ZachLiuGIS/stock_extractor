import pandas as pd


def percentage_string_to_number(df, columns, type_='float'):
    if not isinstance(columns, list):
        columns = [columns]
    for column in columns:
        df[column].replace('\+|%', '', regex=True, inplace=True)
        df[column].replace('unch', '0', inplace=True)
        df[column] = df[column].astype(type_) / 100
