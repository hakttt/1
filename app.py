import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import ta

# Dosyadan tickerları oku
def load_tickers(path):
    with open(path, "r") as f:
        tickers = f.read().strip().split("-")
    return tickers

tickers_nasdaq = load_tickers("tickers_nasdaq.txt")
tickers_nyse = load_tickers("tickers_nyse.txt")

# LRC hesaplama fonksiyonu
def linear_regression_channel(df, length=300):
    if len(df) < length:
        return None, None
    y = df['Close'][-length:].values
    x = np.arange(length)
    coeffs = np.polyfit(x, y, 1)
    slope, intercept = coeffs
    y_fit = slope * x + intercept
    resid = y - y_fit
    std_dev = np.std(resid)
    upper = y_fit + std_dev
    lower = y_fit - std_dev
    return upper, lower

# LRC kesişme kontrolü
def check_lrc_cross(df, lookback=20):
    if len(df) < 300 + lookback:
        return None
    upper, lower = linear_regression_channel(df, 300)
    if upper is None or lower is None:
        return None
    close = df['Close']
    for i in range(lookback):
        if close.iloc[-i-2] < upper[-i-2] and close.iloc[-i-1] > upper[-i-1]:
            return "Cross Over"
        if close.iloc[-i-2] > lower[-i-2] and close.iloc[-i-1] < lower[-i-1]:
            return "Cross Under"
    return None

# Tek SAR sinyali (basit örnek)
def check_sar_signal(df):
    if len(df) < 2:
        return None
    sar = ta.trend.PSARIndicator(df['High'], df['Low'], df['Close'], step=0.02, max_step=0.2)
    sar_values = sar.psar()
    close = df['Close']
    # Son bar için sar altı veya üstü sinyal basit kontrolü
    if close.iloc[-2] < sar_values.iloc[-2] and close.iloc[-1] > sar_values.iloc[-1]:
        return "SAR Cross Up"
    if close.iloc[-2] > sar_values.iloc[-2] and close.iloc[-1] < sar_values.iloc[-1]:
        return "SAR Cross Down"
    return None

# Streamlit başlığı ve ayarlar
st.title("NASDAQ & NYSE LRC ve Tek SAR Tarayıcı")

interval_map = {
    "1 Week": "1wk",
    "3 Days": "3d",
    "1 Day": "1d",
    "4 Hours": "4h"
}

selected_interval = st.selectbox("Zaman Dilimini Seçiniz", list(interval_map.keys()), index=1)
exchange = st.radio("Borsa Seçiniz", ["NASDAQ", "NYSE"])
lookback = st.number_input("Son Kaç Barda Kesişme Ara", min_value=1, max_value=50, value=20, step=1)
scan_lrc = st.checkbox("LRC Kesişmelerini Tara", value=True)
scan_sar = st.checkbox("Tek SAR Sinyallerini Tara", value=False)

if st.button("Taramayı Başlat"):

    tickers = tickers_nasdaq if exchange == "NASDAQ" else tickers_nyse
    st.info(f"{exchange} borsasında {len(tickers)} hisse, {selected_interval} zaman diliminde, son {lookback} bardaki sinyaller aranıyor...")

    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period="300d", interval=interval_map[selected_interval], progress=False)
            if df.empty:
                continue

            # LRC kontrolü
            if scan_lrc:
                lrc_signal = check_lrc_cross(df, lookback)
                if lrc_signal:
                    results.append({
                        "Ticker": ticker,
                        "Signal": lrc_signal,
                        "Type": "LRC",
                        "Price": df['Close'].iloc[-1]
                    })

            # SAR kontrolü
            if scan_sar:
                sar_signal = check_sar_signal(df)
                if sar_signal:
                    results.append({
                        "Ticker": ticker,
                        "Signal": sar_signal,
                        "Type": "SAR",
                        "Price": df['Close'].iloc[-1]
                    })

        except Exception as e:
            # İstersen hata logla: st.error(f"{ticker} için hata: {e}")
            pass

    if results:
        df_res = pd.DataFrame(results)
        st.success(f"{len(results)} sinyal bulundu.")
        st.dataframe(df_res)
    else:
        st.warning("Hiç sinyal bulunamadı.")
