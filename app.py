import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import concurrent.futures

st.set_page_config(page_title="Radar Saham 3-in-1", layout="wide")
st.title("🚀 Master Screener Saham 3-in-1")
st.markdown("Mencari Peluang: **⭐ Trend Follower | ✅ Pullback (Diskon) | 🔥 Bottom Fishing**")

stocks = [
    "BBCA", "DCII", "BBRI", "BYAN", "BMRI", "BREN", "AMMN", "MORA", "TLKM", "DSSA",
    "ASII", "SRAJ", "TPIA", "DNET", "BRPT", "SMMA", "BBNI", "EMAS", "MPRO", "CASA",
    "UNTR", "AADI", "CUAN", "PANI", "BRMS", "ICBP", "ANTM", "ADRO", "HMSP", "IMPC",
    "MDKA", "CDIA", "BNLI", "ISAT", "BUMI", "ADMR", "BRIS", "INDF", "UNVR", "NCKL",
    "AMRT", "MBMA", "PGUN", "SUPR", "CPIN", "BDMN", "PTRO", "GEMS", "MEGA", "INKP",
    "INCO", "MLPT", "EXCL", "BNGA", "PGEO", "BELI", "TAPG", "PTBA", "MTEL", "KLBF",
    "MEDC", "CMRY", "GGRM", "PGAS", "GOTO", "ARCI", "TINS", "TBIG", "MYOR", "AKRA",
    "JARR", "ITMG", "VKTR", "NISP", "TOWR", "FAPA", "ENRG", "BTPN", "MAPI", "MGLV",
    "SILO", "BINA", "MIKA", "SMAR", "JPFA", "FORU", "SRTG", "EMTK", "TKIM", "LIFE",
    "MDIY", "ULTJ", "AVIA", "GIAA", "ADES", "MKPI", "PNBN", "CBDK", "JSMR", "SINI",
    "BNBR", "BSIM", "MAPA", "NSSS", "INTP", "BBHI", "FASW", "SOHO", "PACK", "SUPA",
    "BUVA", "AUTO", "AALI", "DSNG", "BBSI", "POWR", "JRPT", "DEWA", "BBTN", "INDY",
    "MLBI", "PSAB", "BNII", "BFIN", "RAJA", "SMMT", "STAA", "BSSR", "CITA", "BSWD",
    "RLCO", "PWON", "MCOL", "CMNT", "CARE", "SGER", "TSPC", "ALII", "HRUM", "IBST",
    "SCMA", "BSDE", "GOOD", "STTP", "TRIO", "POLU", "RATU", "MSIN", "ARTO", "CLEO",
    "SMGR", "SIDO", "PRAY", "YUPI", "ADMF", "AGII", "BUKA", "SSMS", "LSIP", "CTRA",
    "ESSA", "HRTA", "COIN", "ERAA", "SMSM", "RISE", "EDGE", "CMNP", "BKSL", "HEAL",
    "PLIN", "MIDI", "DUTI", "DMAS", "BHAT", "SIMP", "BMAS", "PKPK", "VICI", "BBMD",
    "BBKP", "WIKA", "TCPI", "BIPI", "MBSS", "TLDN", "SSIA", "ARKO", "BJBR", "NATO",
    "SGRO", "BJTM", "WIFI", "BTPS", "ABMM", "CNMA", "TMAS", "RMKE", "SHIP", "CLAY",
    "EPMT", "INPP", "SMCB", "SMDR", "FORE", "CYBR", "GMFI", "FILM", "YULE", "PNLF",
    "MTDL", "BOGA", "OMED", "WSKT", "UNSP", "UNIC", "DMND", "ACES", "INET", "BALI",
    "WBSA", "TUGU", "ELPI", "MDIA", "BULL", "MTLA", "TRIM", "JECX", "TOTL", "MAYA",
    "HATM", "SAME", "ANJT", "TFCO", "DAAZ", "APIC", "MSJA", "TGKA", "MMIX", "ELSA",
    "MPMX", "DRMA", "KPIG", "MARK", "GJTL", "KRAS", "GGRP", "BPII", "SURE", "MASB",
    "PALM", "LINK", "IFSH", "SMIL", "META", "AMAR", "MSTI", "SOCI", "JTPE", "SMRA",
    "BIRD", "PBID", "CASS", "NICL", "TOBA", "DKFT", "NIRO", "ARGO", "ARNA", "ROCK",
    "TBLA", "NOBU", "PSGO", "MKAP", "ALKA", "UANG", "TEBE", "BANK", "LPPF", "NEST",
    "EURO", "BEEF", "GOTOM", "ROTI", "IMAS", "VISI", "LPKR", "SAMF", "BLTZ", "IATA",
    "BWPT", "RDTX", "AGRO", "ASGR", "CBRE", "KEJU", "WIIM", "ALDO", "GOLF", "JSPT",
    "MAPB", "KIJA", "BTEL", "ISSP", "KEEN", "ABDA", "SRIL", "SDRA", "INPC", "BESS",
    "HEXA", "ASLI", "SKRN", "MDLA", "CENT", "PRDA", "FISH", "FPNI", "OMRE", "CBUT",
    "AGRS", "BIKE", "PNIN", "DAYA", "BNBA", "SFAN", "LPCK", "RALS", "PORT", "BBYB",
    "PNGO", "MGRO", "PBSA", "PYFA", "BGTG", "BUKK", "WINS", "KETR", "TOTO", "TRAM",
    "MCOR", "CPRO", "APLN", "KAEF", "JAWA", "MAHA", "VICO", "BCIC", "CTBN", "ASRI",
    "SCCO", "RIMO", "MYOH", "PSKT", "RANS", "SMDM", "HUMI", "ASSA", "BACA", "PSSI",
    "BISI", "DOOH", "NICE", "AYAM", "DNAR", "MBAP", "MINA", "DATA", "BRAM", "MMLP",
    "SONA", "GTSI", "KINO", "UCID", "MTMH", "PTSN", "BHIT", "KMTR", "IFII", "AMAG",
    "DWGL", "LPGI", "IPCC", "RONY", "DGWG", "IRSX", "PMJS", "IMJS", "BOLT", "MNCN",
    "STAR", "FAST", "COCO", "BLES", "AGAR", "INDR", "POLI", "DVLA", "NICK", "DOID"
]

@st.cache_data(ttl=3600)
def get_benchmark():
    start_date = datetime.today() - timedelta(days=3650)
    end_date = datetime.today()
    try:
        bench_data = yf.download(["^JKSE", "^GSPC"], start=start_date, end=end_date, progress=False)['Close']
        return bench_data.pct_change().dropna()
    except:
        return pd.DataFrame()

def analisis_saham(ticker, bench_returns):
    symbol = f"{ticker}.JK"
    hasil = None
    start_date = datetime.today() - timedelta(days=3650)
    end_date = datetime.today()
    
    try:
        df = yf.download(symbol, start=start_date, end=end_date, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        if not df.empty and len(df) >= 200:
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_200'] = df['Close'].rolling(window=200).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['STD_20'] = df['Close'].rolling(window=20).std()
            df['Lower_BB'] = df['SMA_20'] - (2 * df['STD_20'])
            
            df['H-L'] = df['High'] - df['Low']
            df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
            df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
            df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
            df['ATR'] = df['TR'].rolling(window=14).mean()
            
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/14, adjust=False).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
            
            df['Return'] = df['Close'].pct_change()
            beta_ihsg, beta_sp500 = 0.0, 0.0
            
            if not bench_returns.empty:
                aligned_data = pd.concat([df['Return'], bench_returns], axis=1).dropna()
                if not aligned_data.empty and len(aligned_data) > 50:
                    cov_ihsg = np.cov(aligned_data['Return'], aligned_data['^JKSE'])[0, 1]
                    var_ihsg = np.var(aligned_data['^JKSE'], ddof=1)
                    beta_ihsg = cov_ihsg / var_ihsg if var_ihsg != 0 else 0

            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            PP = (prev['High'] + prev['Low'] + prev['Close']) / 3
            S1 = (2 * PP) - prev['High']
            entry_ideal = (PP + S1) / 2
            if last['Close'] < entry_ideal:
                entry_ideal = last['Close']
            
            target_reversal = int(last['SMA_20'])
            target_trend = int(entry_ideal + (4 * last['ATR']))
            stop_loss = int(entry_ideal - (1.5 * last['ATR']))
            
            rata_volume = df['Volume'].tail(20).mean()
            volume_hari_ini_juta = round(last['Volume'] / 1000000, 1)
            
            if rata_volume < 1000000:
                return None
                
            kriteria_trend = (last['Close'] > last['MA_200']) and (last['MA_50'] > last['MA_200']) and (last['MACD'] > last['Signal_Line']) and (prev['MACD'] <= prev['Signal_Line'])
            kriteria_pullback = (last['Close'] > last['MA_200']) and (last['MA_50'] > last['MA_200']) and (30 <= last['RSI'] <= 45)
            kriteria_bottom = (last['Close'] <= last['Lower_BB'] * 1.01) and (last['RSI'] < 30)
            kriteria_reversal = (last['MACD'] > last['Signal_Line']) and (prev['MACD'] <= prev['Signal_Line']) and (last['MACD'] < 0)
            kriteria_c_gabungan = kriteria_bottom or kriteria_reversal

            kategori = ""
            target_final = target_reversal
            
            if kriteria_trend:
                kategori = "⭐ Trend Follower"
                target_final = target_trend
            elif kriteria_pullback:
                kategori = "✅ Pullback"
                target_final = target_reversal
            elif kriteria_c_gabungan:
                kategori = "🔥 Bottom Fishing" if kriteria_bottom else "🔥 Awal Reversal"
                target_final = target_reversal

            if kategori != "":
                hasil = {
                    "Saham": ticker,
                    "Kategori Strategi": kategori,
                    "Beta IHSG": round(beta_ihsg, 2),
                    "RSI": round(last['RSI'], 1),
                    "Vol(Jt)": volume_hari_ini_juta,
                    "Harga": int(last['Close']),
                    "ANTRE Beli": int(entry_ideal),
                    "Target": target_final,
                    "Cut Loss": stop_loss
                }
    except Exception:
        pass 
    return hasil

if st.button("Jalankan Radar Sekarang (Klik 1x Saja)"):
    with st.spinner('Mesin Server sedang memindai 400 saham (Proses 1-2 menit)...'):
        bench_returns = get_benchmark()
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(analisis_saham, stock, bench_returns): stock for stock in stocks}
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    results.append(res)
                    
        if results:
            res_df = pd.DataFrame(results)
            res_df = res_df.sort_values(by=["Kategori Strategi", "RSI"], ascending=[False, True])
            st.success("✅ Pemindaian Selesai! Berikut rekomendasi sistem:")
            st.dataframe(res_df, use_container_width=True)
        else:
            st.warning("⚠️ Tidak ada saham yang memenuhi 3 kriteria kuat saat ini (Kondisi Wait & See).")
