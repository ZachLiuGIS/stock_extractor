import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


# Normalize data
def normalize_data(df):
    return df / df.ix[0]


# Calculate Daily Returns
def calculate_daily_returns(df):
    daily_return = df/df.shift(1) - 1
    daily_return.ix[0] = 0
    return daily_return


# Calculate Accumulated Returns
def calculate_cumulative_returns(df):
    cum_return = df/df.ix[0] - 1
    return cum_return


def get_bolinger_value(df):
    df = (df - pd.rolling_mean(df, 20)) / (2 * pd.rolling_std(df, 20))
    return df


def get_latest_bolinger_value(symbols):
    if isinstance(symbols, str):
        symbols = [symbols]
    today = datetime.date.today()
    end = str(today)
    start = str(today + relativedelta(months=-2))

    df = get_yahoo_data(symbols, start, end)
    df = (df - pd.rolling_mean(df, 20)) / (2 * pd.rolling_std(df, 20))
    print(df.ix[-1])
    return df.ix[-1]


# Calculate Portfolio Value
def get_portfolio_value(prices, allocs, start_val=1):
    norm_prices = normalize_data(prices)
    alloc_norm_prices = norm_prices * allocs
    port_val = (alloc_norm_prices * start_val).sum(axis=1)
    return port_val


def plot_normalized_data(df, title="Normalized prices", xlabel="Date", ylabel="Normalized price"):
    """Normalize given stock prices and plot for comparison.

    Parameters
    ----------
        df: DataFrame containing stock prices to plot (non-normalized)
        title: plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    df = normalize_data(df)
    plot_data(df, title, xlabel, ylabel)


def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    """Calculate statistics on given portfolio values.

    Parameters
    ----------
        port_val: daily portfolio value
        daily_rf: daily risk-free rate of return (default: 0%)
        samples_per_year: frequency of sampling (default: 252 trading days)

    Returns
    -------
        cum_ret: cumulative return
        avg_daily_ret: average of daily returns
        std_daily_ret: standard deviation of daily returns
        sharpe_ratio: annualized Sharpe ratio
    """
    cum_ret = calculate_cumulative_returns(port_val).ix[-1]
    daily_rets = calculate_daily_returns(port_val).ix[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = samples_per_year ** 0.5 * avg_daily_ret / std_daily_ret
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio


def symbol_to_path(symbol, base_dir=os.path.join("..", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, start_date, end_date, add_spy=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    if add_spy and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
    return df


# Get stock data from yahoo finance
def get_yahoo_data(symbols, start, end, use_volumns=False, add_spy=False):
    dates = pd.date_range(start, end)
    df = pd.DataFrame(index=dates)

    # add SPY for reference, if absent
    if 'SPY' not in symbols:
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = web.DataReader(symbol, 'yahoo', start, end)
        if use_volumns:
            df_temp = df_temp[['Adj Close', 'Volume']]
            df_temp = df_temp.rename(columns={'Adj Close': symbol, 'Volume': 'Volume_' + symbol})
        else:
            df_temp = df_temp[['Adj Close']]
            df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)

        # drop dates SPY did not trade
        if symbol == 'SPY':
            df = df.dropna(subset=["SPY"])

    if not add_spy:
        del df['SPY']

    return df
