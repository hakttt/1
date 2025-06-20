import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta

st.set_page_config(page_title="LRC & Tek SAR Tarayıcı", layout="wide")

# --- Tüm Ticker Listeleri ---
with open("tickers_nyse.txt", "r") as f:
    tickers_nyse = f.read().strip().split("-")

with open("tickers_nasdaq.txt", "r") as f:
    tickers_nasdaq = f.read().strip().split("-")


# --- LRC Hesaplama Fonksiyonu ---
def calculate_lrc_channel(df, length=300):
    if len(df) < length:
        return None, None

    y = df['Close'][-length:].values
    x = np.arange(length)
    coeffs = np.polyfit(x, y, 1)
    y_fit = coeffs[0] * x + coeffs[1]
    std_dev = np.std(y - y_fit)
    upper = y_fit + std_dev
    lower = y_fit - std_dev
    return upper, lower

# --- LRC Kesişme Kontrolü ---
def check_lrc_cross(df, bars_to_check=20):
    upper, lower = calculate_lrc_channel(df)
    if upper is None or lower is None:
        return None

    closes = df['Close'].values
    signal = None
    for i in range(bars_to_check):
        if closes[-i-2] < upper[-i-2] and closes[-i-1] > upper[-i-1]:
            signal = ("Cross Over", df.index[-i-1].strftime("%Y-%m-%d"))
            break
        elif closes[-i-2] > lower[-i-2] and closes[-i-1] < lower[-i-1]:
            signal = ("Cross Under", df.index[-i-1].strftime("%Y-%m-%d"))
            break
    return signal


# --- SAR Tespiti ---
def check_tek_sar(df, bars_to_check=20):
    if len(df) < bars_to_check + 2:
        return None

    df['SAR'] = ta.trend.PSARIndicator(high=df['High'], low=df['Low'], close=df['Close']).psar()

    sar = df['SAR'].values
    close = df['Close'].values
    signal = None
    for i in range(bars_to_check):
        prev_close, curr_close = close[-i-2], close[-i-1]
        prev_sar, curr_sar = sar[-i-2], sar[-i-1]

        # SAR aşağıdan yukarı keserse sinyal
        if prev_close < prev_sar and curr_close > curr_sar:
            signal = ("SAR Cross Over", df.index[-i-1].strftime("%Y-%m-%d"))
            break
        elif prev_close > prev_sar and curr_close < curr_sar:
            signal = ("SAR Cross Under", df.index[-i-1].strftime("%Y-%m-%d"))
            break
    return signal


# --- Streamlit Arayüz ---
st.title("📈 LRC ve Tek SAR Tarayıcı")

exchange = st.radio("Borsa", ["NASDAQ", "NYSE"])
interval_map = {
    "1 Hafta": "1wk",
    "3 Gün": "3d",
    "1 Gün": "1d",
    "4 Saat": "4h"
}
interval_label = st.selectbox("Zaman Dilimi", list(interval_map.keys()))
interval = interval_map[interval_label]

scan_mode = st.radio("Tarama Türü", ["Sadece LRC", "Sadece Tek SAR", "Her İkisi"])
bars_to_check = st.slider("Son kaç bar taransın?", 5, 100, 20)

if st.button("🔍 Taramayı Başlat"):
    st.info("Veriler indiriliyor ve analiz ediliyor...")

    tickers = tickers_nasdaq if exchange == "NASDAQ" else tickers_nyse
    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period="300d", interval=interval, progress=False)
            if df.empty:
                continue

            entry = {"Ticker": ticker}

            if scan_mode in ["Sadece LRC", "Her İkisi"]:
                lrc = check_lrc_cross(df, bars_to_check)
                if lrc:
                    entry["LRC"] = lrc[0]
                    entry["LRC Date"] = lrc[1]

            if scan_mode in ["Sadece Tek SAR", "Her İkisi"]:
                sar = check_tek_sar(df, bars_to_check)
                if sar:
                    entry["SAR"] = sar[0]
                    entry["SAR Date"] = sar[1]

            if "LRC" in entry or "SAR" in entry:
                results.append(entry)

        except Exception as e:
            st.error(f"{ticker} için hata: {e}")
            continue

    if results:
        df_result = pd.DataFrame(results)
        st.success(f"{len(results)} sonuç bulundu.")
        st.dataframe(df_result)
    else:
        st.warning("Hiçbir sinyal bulunamadı.")
