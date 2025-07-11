import yfinance as yf
import pandas as pd
import numpy as np

def download_data(ticker, period="10y", interval="1d"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        return None

def create_3d_bars(df_1d):
    bars = []
    for i in range(0, len(df_1d) - 2, 3):
        chunk = df_1d.iloc[i:i+3]
        bar = {
            "Open": chunk["Open"].iloc[0],
            "High": chunk["High"].max(),
            "Low": chunk["Low"].min(),
            "Close": chunk["Close"].iloc[-1],
            "Volume": chunk["Volume"].sum(),
            "Date": chunk.index[-1]
        }
        bars.append(bar)
    return pd.DataFrame(bars).set_index("Date")

def calculate_lrc(df, length=300):
    x = np.arange(length)
    y_high = df["High"].tail(length).values
    y_low = df["Low"].tail(length).values

    high_fit = np.polyfit(x, y_high, 1)
    low_fit = np.polyfit(x, y_low, 1)

    high_line = high_fit[0] * x + high_fit[1]
    low_line = low_fit[0] * x + low_fit[1]

    return high_line, low_line

def find_lrc_cross(df, lookback_bars=20, lrc_length=300):
    crosses = []
    if len(df) < lrc_length + lookback_bars:
        return crosses

    df = df[-(lrc_length + lookback_bars):].copy().reset_index(drop=True)
    for i in range(lookback_bars):
        window = df.iloc[i:i + lrc_length]
        if len(window) < lrc_length:
            continue

        x = np.arange(lrc_length)
        h_line, l_line = calculate_lrc(window, lrc_length)
        if h_line[-2] < l_line[-2] and h_line[-1] > l_line[-1]:
            crosses.append((df["Date"].iloc[i + lrc_length - 1], "CROSSOVER"))
        elif h_line[-2] > l_line[-2] and h_line[-1] < l_line[-1]:
            crosses.append((df["Date"].iloc[i + lrc_length - 1], "CROSSUNDER"))

    return crosses
