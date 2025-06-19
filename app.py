import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# ==========================
# Kullanıcı Ayarları Paneli
# ==========================

st.title("📈 LRC & Tek SAR Sinyal Tarayıcı")

scan_type = st.multiselect(
    "Tarama türünü seçin:",
    options=["LRC Kesişme", "Tek SAR"],
    default=["LRC Kesişme"]
)

interval_map = {
    "1 Week": "1wk",
    "3 Days": "3d",
    "1 Day": "1d",
    "4 Hours": "4h"
}
interval_label = st.selectbox("Zaman dilimi:", list(interval_map.keys()))
interval = interval_map[interval_label]

lookback_bars = st.slider("Kaç bar içinde sinyal aransın?", min_value=5, max_value=100, value=20)

exchange = st.radio("Borsa Seçimi", ["NASDAQ", "NYSE"])

# ======================
# NYSE ve NASDAQ Ticker
# ======================

# Uzun ticker listelerini dış dosyadan çekiyorsan buraya import et
# Veya aşağıya yapıştır (tamamını aşağı sığdırmak yerine dış dosya mantıklıdır)
from tickers import tickers_nasdaq, tickers_nyse

tickers = tickers_nasdaq if exchange == "NASDAQ" else tickers_nyse
# Ticker listeleri (tam versiyon)
tickers_nyse = """A-AA-AAP-ABBV-ABR-ABT-ACHR-ACI-ACM-ACN-ACVA-ADC-ADM-ADNT-ADT-AEE-AEG-AEM-AEO-AER-AES-AESI-AFL-AG-AGI-AGL-AHR-AI-AIG-AJG-AKR-ALB-ALC-ALK-ALL-ALLY-AM-AMCR-AME-AMH-AMPS-AMT-AMTM-AMX-ANET-ANF-AON-AOS-APD-APG-APH-APLE-APO-APTV-AQN-AR-ARCO-ARE-ARES-ARI-ARMK-AROC-ARR-AS-ASAN-ASB-ASPN-ASX-ATEN-ATI-AU-AUB-AVTR-AWK-AXP-AXTA-AZEK-BA-BABA-BAC-BAH-BALL-BAM-BANC-BAX-BBVA-BBWI-BBY-BCE-BCS-BDX-BE-BEKE-BEN-BEPC-BERY-BF.B-BG-BGS-BHP-BHVN-BILL-BIRK-BJ-BK-BKD-BLDR-BMY-BN-BNL-BNS-BOX-BP-BRBR-BRK.B-BRO-BROS-BRX-BSX-BTI-BTU-BUD-BURL-BVN-BWA-BX-BXMT-BXP-BXSL-C-CADE-CAG-CAH-CARR-CAT-CAVA-CB-CBRE-CC-CCI-CCJ-CCK-CCL-CDE-CDP-CE-CF-CFG-CHD-CHWY-CI-CIEN-CIVI-CL-CLF-CLS-CLX-CM-CMA-CMC-CMG-CMS-CNC-CNH-CNI-CNK-CNM-CNP-CNQ-CNX-COF-COHR-COLD-COMP-COP-COR-COTY-COUR-CP-CPNG-CPRI-CRBG-CRGY-CRH-CRI-CRK-CRL-CRM-CSTM-CTRA-CTRE-CTVA-CUBE-CUK-CUZ-CVE-CVI-CVNA-CVS-CVX-CWAN-CWH-CWK-CX-CXM-CXW-D-DAL-DAN-DAR-DAY-DB-DBRG-DD-DE-DEA-DECK-DEI-DELL-DEO-DESP-DFS-DG-DGX-DHI-DHR-DHT-DINO-DIS-DK-DKS-DLR-DNA-DNB-DNOW-DOC-DOCN-DOCS-DOW-DRH-DRI-DT-DTE-DTM-DUK-DV-DVN-DX-DXC-EAT-EBR-EC-ECC-ECL-ED-EDU-EFC-EFX-EGO-EIX-EL-ELAN-ELF-ELS-ELV-EMN-EMR-ENB-ENFN-EOG-EPD-EPRT-EQH-EQNR-EQR-EQT-ERJ-ES-ESI-ESRT-ESTC-ET-ETN-ETR-EVH-EW-EXPD-EXR-F-FBIN-FBP-FCX-FDX-FE-FERG-FHN-FI-FIS-FL-FLG-FLO-FLR-FLS-FLUT-FMC-FNA-FNB-FND-FNF-FOUR-FR-FRO-FSK-FSLY-FSM-FTI-FTV-FUN-G-GAP-GD-GDDY-GE-GENI-GEO-GES-GEV-GFI-GFL-GIS-GLW-GM-GME-GMED-GNL-GNW-GOF-GOLD-GPC-GPK-GPN-GRND-GS-GSK-GTES-GXO-HAL-HASI-HAYW-HBM-HCA-HD-HDB-HE-HES-HESM-HIG-HIMS-HIW-HL-HLF-HLN-HLT-HLX-HMC-HMY-HOG-HOMB-HP-HPE-HPQ-HR-HRB-HRL-HSBC-HSY-HTGC-HUM-HUN-HWM-HXL-IAG-IBM-IBN-ICE-IFF-IGT-INFA-INFY-ING-INVH-IONQ-IOT-IP-IPG-IQV-IRDM-IREN-ISRG-JD-KC-KDP-KHC-KLAC-KROS-KTOS-KURA-LBTYA-LBTYK-LEGN-LFST-LI-LIN-LINE-LITE-LKQ-LNT-LRCX-LSCC-LULU-LUNR-LX-LYFT-LZ-MAR-MARA-MAT-MBLY-MCHP-MCW-MDB-MDLZ-META-MGNI-MKSI-MNMD-MNST-MOMO-MRNA-MRVL-MSFT-MSTR-MTCH-MU-MXL-NAMS-NBIS-NBIX-NCNO-NDAQ-NEO-NEOG-NEXT-NFE-NFLX-NMRK-NN-NNE-NTAP-NTES-NTLA-NTNX-NTRA-NTRS-NVAX-NVDA-NWSA-NXPI-NXT-OCUL-ODFL-OKTA-OLLI-ON-ONB-OPCH-OS-OTEX-OUST-OZK-PAA-PAGP-PANW-PARA-PAYO-PAYX-PCAR-PCT-PCVX-PDCO-PDD-PENN-PEP-PFG-PGNY-PGY-PINC-PLAY-PLTR-PLYA-PONY-PPC-PRCH-PTC-PTEN-PTLO-PTON-PYPL-PZZA-QCOM-QFIN-QRVO-QUBT-QURE-RCAT-RCKT-RDFN-REG-RELY-RGTI-RIOT-RIVN-RKLB-RNA-ROIV-ROKU-ROST-RPRX-RUM-RUN-RVMD-RXRX-RYAAY-SAGE-SATS-SBLK-SBRA-SBUX-SEDG-SERV-SFM-SGRY-SHC-SHOO-SHOP-SIRI-SLM-SMCI-SMMT-SMPL-SMTC-SNDX-SNPS-SNY-SOFI-SONO-SOUN-SPRY-SRAD-SRPT-SRRK-SSNC-SSRM-STLD-STNE-STX-SWKS-SWTX-SYM-TCOM-TEAM-TECH-TEM-TENB-TER-TGTX-TIGR-TLN-TMDX-TMUS-TNDM-TPG-TRIP-TRMB-TRMD-TROW-TRVI-TSCO-TSLA-TTD-TTEK-TTWO-TVTX-TW-TWST-TXG-TXN-TXRH-UAL-UDMY-ULTA-UPST-UPWK-URBN-VERX-VIAV-VIR-VITL-VKTX-VLY-VNET-VNOM-VOD-VRNA-VRNS-VRRM-VRTX-VSAT-VTRS-WAY-WB-WBA-WBD-WDAY-WDC-WEN-WFRD-WMG-WRD-WSC-WVE-WYNN-XEL-XP-XRAY-Z-ZI-ZION-ZM-ZS""".strip().split("-")

tickers_nasdaq = """AAL-AAOI-AAPL-ABNB-ACAD-ACGL-ACHC-ACMR-ADBE-ADI-ADMA-ADP-ADPT-ADSK-ADTN-AEP-AFRM-AGNC-AHCO-AKAM-AKRO-ALAB-ALGM-ALHC-ALKS-ALKT-AMAT-AMD-AMGN-AMKR-AMRX-AMZN-APA-APLD-APLS-APP-ARCC-ARHS-ARM-ARQT-ARVN-ARWR-ASML-ASO-ASPI-ASTS-ATAT-ATEC-ATSG-AUPH-AUR-AVDL-AVDX-AVGO-AVPT-AVXL-AZN-BBIO-BCRX-BEAM-BECN-BGC-BIDU-BIIB-BILI-BKR-BLMN-BMRN-BRKR-BRZE-BSY-BTDR-BTSG-BZ-CAKE-CAPR-CAR-CARG-CART-CCCS-CCEP-CDNS-CDW-CEG-CELH-CENX-CERT-CFLT-CG-CGNX-CHRW-CHTR-CHX-CLBT-CLMT-CLSK-CMCSA-CME-CMRX-COIN-COLB-COO-CORT-CORZ-COST-CPB-CPRT-CPRX-CRDO-CRMD-CRNC-CROX-CRSP-CRWD-CSCO-CSGP-CSIQ-CSX-CTAS-CTSH-CYTK-CZR-DASH-DAWN-DBX-DDOG-DJT-DKNG-DLTR-DNLI-DOCU-DVAX-DXCM-DYN-EA-EBAY-EBC-EH-ENPH-ENTG-ENVX-ERIC-ETNB-ETSY-EVRG-EWBC-EWTX-EXAS-EXC-EXE-EXEL-EXLS-EXPE-EXPI-EXTR-EYE-FA-FANG-FAST-FITB-FIVE-FIVN-FLEX-FLYW-FOLD-FOX-FOXA-FRPT-FRSH-FSLR-FTAI-FTNT-FTRE-FULT-FUTU-FWONK-FYBR-GBDC-GCT-GDS-GEHC-GEN-GFS-GGAL-GH-GILD-GLBE-GLNG-GLPI-GMAB-GNTX-GO-GOGL-GOGO-GOOG-GOOGL-GRAL-GRFS-GRPN-GRRR-GT-GTLB-GTX-HALO-HAS-HBAN-HIMX-HLIT-HLMN-HOLX-HON-HOOD-HSAI-HSIC-HST-HTHT-HUT-IAC-IBKR-ICLR-IDYA-ILMN-IMNM-IMVT-INCY-INDV-INMD-INOD-INSM-INTC-INTR-INTU-IONS-IRDM-IREN-ISRG-JD-KC-KDP-KHC-KLAC-KROS-KTOS-KURA-LBTYA-LBTYK-LEGN-LFST-LI-LIN-LINE-LITE-LKQ-LNT-LRCX-LSCC-LULU-LUNR-LX-LYFT-LZ-MAR-MARA-MAT-MBLY-MCHP-MCW-MDB-MDLZ-META-MGNI-MKSI-MNMD-MNST-MOMO-MRNA-MRVL-MSFT-MSTR-MTCH-MU-MXL-NAMS-NBIS-NBIX-NCNO-NDAQ-NEO-NEOG-NEXT-NFE-NFLX-NMRK-NN-NNE-NTAP-NTES-NTLA-NTNX-NTRA-NTRS-NVAX-NVDA-NWSA-NXPI-NXT-OCUL-ODFL-OKTA-OLLI-ON-ONB-OPCH-OS-OTEX-OUST-OZK-PAA-PAGP-PANW-PARA-PAYO-PAYX-PCAR-PCT-PCVX-PDCO-PDD-PENN-PEP-PFG-PGNY-PGY-PINC-PLAY-PLTR-PLYA-PONY-PPC-PRCH-PTC-PTEN-PTLO-PTON-PYPL-PZZA-QCOM-QFIN-QRVO-QUBT-QURE-RCAT-RCKT-RDFN-REG-RELY-RGTI-RIOT-RIVN-RKLB-RNA-ROIV-ROKU-ROST-RPRX-RUM-RUN-RVMD-RXRX-RYAAY-SAGE-SATS-SBLK-SBRA-SBUX-SEDG-SERV-SFM-SGRY-SHC-SHOO-SHOP-SIRI-SLM-SMCI-SMMT-SMPL-SMTC-SNDX-SNPS-SNY-SOFI-SONO-SOUN-SPRY-SRAD-SRPT-SRRK-SSNC-SSRM-STLD-STNE-STX-SWKS-SWTX-SYM-TCOM-TEAM-TECH-TEM-TENB-TER-TGTX-TIGR-TLN-TMDX-TMUS-TNDM-TPG-TRIP-TRMB-TRMD-TROW-TRVI-TSCO-TSLA-TTD-TTEK-TTWO-TVTX-TW-TWST-TXG-TXN-TXRH-UAL-UDMY-ULTA-UPST-UPWK-URBN-VERX-VIAV-VIR-VITL-VKTX-VLY-VNET-VNOM-VOD-VRNA-VRNS-VRRM-VRTX-VSAT-VTRS-WAY-WB-WBA-WBD-WDAY-WDC-WEN-WFRD-WMG-WRD-WSC-WVE-WYNN-XEL-XP-XRAY-Z-ZI-ZION-ZM-ZS""".strip().split("-")

# =====================
# LRC Hesaplama Kısmı
# =====================

def linear_regression_channel(df, length=300):
    if len(df) < length:
        return None, None
    y = df['Close'][-length:].values
    x = np.arange(length)
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    resid = y - y_fit
    std_dev = np.std(resid)
    upper = y_fit + std_dev
    lower = y_fit - std_dev
    return upper, lower

def check_lrc_cross(df, lookback):
    upper, lower = linear_regression_channel(df)
    if upper is None or lower is None:
        return None
    close = df['Close']
    for i in range(lookback, 0, -1):
        if i + 1 >= len(close):
            continue
        # Cross over
        if close.iloc[-i-1] < upper[-i-1] and close.iloc[-i] > upper[-i]:
            return "Cross Over"
        # Cross under
        if close.iloc[-i-1] > lower[-i-1] and close.iloc[-i] < lower[-i]:
            return "Cross Under"
    return None

# ========================
# Tek SAR Kontrol Fonksiyonu
# ========================

def check_single_sar(df, lookback):
    if len(df) < lookback + 2:
        return None
    sar = ta.trend.PSARIndicator(df['High'], df['Low'], df['Close']).psar()
    close = df['Close']
    for i in range(lookback, 0, -1):
        if i + 1 >= len(sar):
            continue
        if close.iloc[-i-1] < sar.iloc[-i-1] and close.iloc[-i] > sar.iloc[-i]:
            return "SAR Long"
        if close.iloc[-i-1] > sar.iloc[-i-1] and close.iloc[-i] < sar.iloc[-i]:
            return "SAR Short"
    return None

# ========================
# Tarama Başlat
# ========================

if st.button("Taramayı Başlat"):
    st.info(f"{len(tickers)} hissede tarama yapılıyor...")

    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period="400d", interval=interval, progress=False)
            if df.empty or len(df) < 50:
                continue

            lrc_signal = None
            sar_signal = None

            if "LRC Kesişme" in scan_type:
                lrc_signal = check_lrc_cross(df, lookback_bars)

            if "Tek SAR" in scan_type:
                sar_signal = check_single_sar(df, lookback_bars)

            if lrc_signal or sar_signal:
                results.append({
                    "Ticker": ticker,
                    "LRC": lrc_signal or "",
                    "SAR": sar_signal or "",
                    "Close": df['Close'].iloc[-1],
                    "Interval": interval
                })
        except Exception as e:
            continue

    if results:
        df_res = pd.DataFrame(results)
        st.success(f"{len(results)} sinyal bulundu.")
        st.dataframe(df_res)
    else:
        st.warning("Hiç sinyal bulunamadı.")
