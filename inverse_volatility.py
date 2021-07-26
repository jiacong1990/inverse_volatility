#!/usr/local/bin/python3

from pandas_datareader import data as pdr
import datetime
import yfinance as yf

yf.pdr_override()


def get_data(ticker, end_date, window):
    start_date = end_date - datetime.timedelta(days=window*2)
    print(f"Grabbing price history for {ticker} as of {end_date} with window size {window} days...")
    df = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
    return df.tail(window+1)


def calculate_volatility(price_history_series):
    log_return = price_history_series.rolling(window=2).apply(lambda x: x[1]/x[0] - 1)

    volatility = log_return.std(skipna=True, ddof=1)
    return volatility


def get_allocations(tickers=[], end_date=None, window_days=None):
    if len(tickers) == 0:
        tickers = ['UPRO', 'TMF']

    if end_date is None:
        end_date = datetime.date.today()

    if window_days is None:
        window_days = 20

    volatility_list = []
    for t in tickers:
        price_history_raw = get_data(t, end_date, window_days)
        close_price_history = price_history_raw['Close']
        print(f"latest close price for {t}: {close_price_history.iloc[-1]:.2f}")
        v = calculate_volatility(close_price_history)
        volatility_list.append(v)

    sum_inverse_volatility = 0
    for v in volatility_list:
        sum_inverse_volatility += 1/v

    allocation_ratios = [100 / x / sum_inverse_volatility for x in volatility_list]

    for i in range(len(tickers)):
        print(f"{tickers[i]}: {allocation_ratios[i]:.2f}%")


if __name__ == '__main__':
    get_allocations()
