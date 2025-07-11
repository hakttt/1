import streamlit as st
from utils import download_data, create_3d_bars, find_lrc_cross

st.set_page_config(layout="wide")
st.title("LRC Kesişme Tarayıcı")

with st.sidebar:
    st.header("Ayarlar")
    lookback = st.slider("Son kaç 3D barda taransın?", 5, 50, 20)
    exchange = st.radio("Borsa", ["NASDAQ", "NYSE"])

    if exchange == "NASDAQ":
        with open("tickers_nasdaq.txt") as f:
            tickers = [line.strip() for line in f if line.strip()]
    else:
        with open("tickers_nyse.txt") as f:
            tickers = [line.strip() for line in f if line.strip()]

    run_scan = st.button("Taramayı Başlat")

if run_scan:
    st.info("Taramaya başlandı...")
    results = []
    for i, ticker in enumerate(tickers):
        df_1d = download_data(ticker)
        if df_1d is None or len(df_1d) < 310:
            continue
        df_3d = create_3d_bars(df_1d)
        cross_signals = find_lrc_cross(df_3d, lookback_bars=lookback)
        if cross_signals:
            last_signal = cross_signals[-1]
            results.append((ticker, last_signal[0].strftime("%Y-%m-%d"), last_signal[1]))
        st.write(f"{i+1}/{len(tickers)} tarandı: {ticker}")

    if results:
        st.success(f"{len(results)} hisse bulundu")
        st.dataframe(results, use_container_width=True)
    else:
        st.warning("Hiçbir kesişme bulunamadı.")
