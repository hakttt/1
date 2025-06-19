import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta

# --- Ticker Listeleri ---
tickers_nyse = "A-AA-AAP-ABBV-ABR-ABT-ACHR-ACI-ACM-ACN-ACVA-ADC-ADM-ADNT-ADT-AEE-AEG-AEM-AEO-AER-AES-AESI-AFL-AG-AGI-AGL-AHR-AI-AIG-AJG-AKR-ALB-ALC-ALK-ALL-ALLY-AM-AMCR-AME-AMH-AMPS-AMT-AMTM-AMX-ANET-ANF-AON-AOS-APD-APG-APH-APLE-APO-APTV-AQN-AR-ARCO-ARE-ARES-ARI-ARMK-AROC-ARR-AS-ASAN-ASB-ASPN-ASX-ATEN-ATI-AU-AUB-AVTR-AWK-AXP-AXTA-AZEK-BA-BABA-BAC-BAH-BALL-BAM-BANC-BAX-BBVA-BBWI-BBY-BCE-BCS-BDX-BE-BEKE-BEN-BEPC-BERY-BF.B-BG-BGS-BHP-BHVN-BILL-BIRK-BJ-BK-BKD-BLDR-BMY-BN-BNL-BNS-BOX-BP-BRBR-BRK.B-BRO-BROS-BRX-BSX-BTI-BTU-BUD-BURL-BVN-BWA-BX-BXMT-BXP-BXSL-C-CADE-CAG-CAH-CARR-CAT-CAVA-CB-CBRE-CC-CCI-CCJ-CCK-CCL-CDE-CDP-CE-CF-CFG-CHD-CHWY-CI-CIEN-CIVI-CL-CLF-CLS-CLX-CM-CMA-CMC-CMG-CMS-CNC-CNH-CNI-CNK-CNM-CNP-CNQ-CNX-COF-COHR-COLD-COMP-COP-COR-COTY-COUR-CP-CPNG-CPRI-CRBG-CRGY-CRH-CRI-CRK-CRL-CRM-CSTM-CTRA-CTRE-CTVA-CUBE-CUK-CUZ-CVE-CVI-CVNA-CVS-CVX-CWAN-CWH-CWK-CX-CXM-CXW-D-DAL-DAN-DAR-DAY-DB-DBRG-DD-DE-DEA-DECK-DEI-DELL-DEO-DESP-DFS-DG-DGX-DHI-DHR-DHT-DINO-DIS-DK-DKS-DLR-DNA-DNB-DNOW-DOC-DOCN-DOCS-DOW-DRH-DRI-DT-DTE-DTM-DUK-DV-DVN-DX-DXC-EAT-EBR-EC-ECC-ECL-ED-EDU-EFC-EFX-EGO-EIX-EL-ELAN-ELF-ELS-ELV-EMN-EMR-ENB-ENFN-EOG-EPD-EPRT-EQH-EQNR-EQR-EQT-ERJ-ES-ESI-ESRT-ESTC-ET-ETN-ETR-EVH-EW-EXPD-EXR-F-FBIN-FBP-FCX-FDX-FE-FERG-FHN-FI-FIS-FL-FLG-FLO-FLR-FLS-FLUT-FMC-FNA-FNB-FND-FNF-FOUR-FR-FRO-FSK-FSLY-FSM-FTI-FTV-FUN-G-GAP-GD-GDDY-GE-GENI-GEO-GES-GEV-GFI-GFL-GIS-GLW-GM-GME-GMED-GNL-GNW-GOF-GOLD-GPC-GPK-GPN-GRND-GS-GSK-GTES-GXO-HAL-HASI-HAYW-HBM-HCA-HD-HDB-HE-HES-HESM-HIG-HIMS-HIW-HL-HLF-HLN-HLT-HLX-HMC-HMY-HOG-HOMB-HP-HPE-HPQ-HR-HRB-HRL-HSBC-HSY-HTGC-HUM-HUN-HWM-HXL-IAG-IBM-IBN-ICE-IFF-IGT-INFA-INFY-ING-INVH-IONQ-IOT-IP-IPG-IQV-IRDM-IREN-ISRG-JD-KC-KDP-KHC-KLAC-KROS-KTOS-KURA-LBTYA-LBTYK-LEGN-LFST-LI-LIN-LINE-LITE-LKQ-LNT-LRCX-LSCC-LULU-LUNR-LX-LYFT-LZ-MAR-MARA-MAT-MBLY-MCHP-MCW-MDB-MDLZ-META-MGNI-MKSI-MNMD-MNST-MOMO-MRNA-MRVL-MSFT-MSTR-MTCH-MU-MXL-NAMS-NBIS-NBIX-NCNO-NDAQ-NEO-NEOG-NEXT-NFE-NFLX-NMRK-NN-NNE-NTAP-NTES-NTLA-NTNX-NTRA-NTRS-NVAX-NVDA-NWSA-NXPI-NXT-OCUL-ODFL-OKTA-OLLI-ON-ONB-OPCH-OS-OTEX-OUST-OZK-PAA-PAGP-PANW-PARA-PAYO-PAYX-PCAR-PCT-PCVX-PDCO-PDD-PENN-PEP-PFG-PGNY-PGY-PINC-PLAY-PLTR-PLYA-PONY-PPC-PRCH-PTC-PTEN-PTLO-PTON-PYPL-PZZA-QCOM-QFIN-QRVO-QUBT-QURE-RCAT-RCKT-RDFN-REG-RELY-RGTI-RIOT-RIVN-RKLB-RNA-ROIV-ROKU-ROST-RPRX-RUM-RUN-RVMD-RXRX-RYAAY-SAGE-SATS-SBLK-SBRA-SBUX-SEDG-SERV-SFM-SGRY-SHC-SHOO-SHOP-SIRI-SLM-SMCI-SMMT-SMPL-SMTC-SNDX-SNPS-SNY-SOFI-SONO-SOUN-SPRY-SRAD-SRPT-SRRK-SSNC-SSRM-STLD-STNE-STX-SWKS-SWTX-SYM-TCOM-TEAM-TECH-TEM-TENB-TER-TGTX-TIGR-TLN-TMDX-TMUS-TNDM-TPG-TRIP-TRMB-TRMD-TROW-TRVI-TSCO-TSLA-TTD-TTEK-TTWO-TVTX-TW-TWST-TXG-TXN-TXRH-UAL-UDMY-ULTA-UPST-UPWK-URBN-VERX-VIAV-VIR-VITL-VKTX-VLY-VNET-VNOM-VOD-VRNA-VRNS-VRRM-VRTX-VSAT-VTRS-WAY-WB-WBA-WBD-WDAY-WDC-WEN-WFRD-WMG-WRD-WSC-WVE-WYNN-XEL-XP-XRAY-Z-ZI-ZION-ZM-ZS".split("-")
tickers_nasdaq = "AAL-AAOI-AAPL-ABNB-ACAD-ACGL-ACHC-ACMR-ADBE-ADI-ADMA-ADP-ADPT-ADSK-ADTN-AEP-AFRM-AGNC-AHCO-AKAM-AKRO-ALAB-ALGM-ALHC-ALKS-ALKT-AMAT-AMD-AMGN-AMKR-AMRX-AMZN-APA-APLD-APLS-APP-ARCC-ARHS-ARM-ARQT-ARVN-ARWR-ASML-ASO-ASPI-ASTS-ATAT-ATEC-ATSG-AUPH-AVDL-AVDX-AVGO-AVPT-AVXL-AZN".split("-")  # Örnek, listeyi kısalttım.

# --- Yardımcı Fonksiyonlar ---

def linear_regression_channel(df, length=300):
    y = df['Close'][-length:].values
    x = np.arange(length)
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    std = np.std(y - y_fit)
    return y_fit[-1] + std, y_fit[-1] - std

def check_lrc_cross(df, lookback):
    upper, lower = linear_regression_channel(df)
    close = df['Close']
    for i in range(lookback):
        if close.iloc[-i-2] < upper and close.iloc[-i-1] > upper:
            return "Cross Over"
        elif close.iloc[-i-2] > lower and close.iloc[-i-1] < lower:
            return "Cross Under"
    return None

def check_sar_flip(df, lookback):
    sar = ta.trend.psar_up(df['High'], df['Low'], df['Close'])
    prev = sar.shift(1)
    for i in range(lookback):
        if pd.notna(prev.iloc[-i-1]) and pd.isna(sar.iloc[-i-1]):
            return "SAR Flip to Long"
        if pd.isna(prev.iloc[-i-1]) and pd.notna(sar.iloc[-i-1]):
            return "SAR Flip to Short"
    return None

# --- Arayüz ---

st.title("📈 LRC & Tek SAR Tarayıcı")

interval_map = {"1W": "1wk", "3D": "3d", "1D": "1d", "4H": "4h"}
exchange = st.selectbox("Borsa", ["NASDAQ", "NYSE"])
interval = st.selectbox("Zaman Dilimi", list(interval_map.keys()))
lookback = st.slider("Kaç bar geriye taransın?", 1, 100, 20)
scan_type = st.multiselect("Tarama türü", ["LRC", "Tek SAR"], default=["LRC"])

if st.button("🔍 Tara"):
    tickers = tickers_nasdaq if exchange == "NASDAQ" else tickers_nyse
    found = []
    st.info(f"{len(tickers)} adet hisse taranıyor...")

    for t in tickers:
        df = yf.download(t, period="400d", interval=interval_map[interval], progress=False)
        if df.empty or len(df) < 100:
            continue

        signal = ""
        if "LRC" in scan_type:
            lrc = check_lrc_cross(df, lookback)
            if lrc:
                signal += lrc

        if "Tek SAR" in scan_type:
            sar = check_sar_flip(df, lookback)
            if sar:
                signal += (" / " if signal else "") + sar

        if signal:
            found.append({"Ticker": t, "Sinyal": signal, "Fiyat": df['Close'].iloc[-1]})

    if found:
        st.success(f"{len(found)} sinyal bulundu.")
        st.dataframe(pd.DataFrame(found))
    else:
        st.warning("Hiçbir sinyal bulunamadı.")
