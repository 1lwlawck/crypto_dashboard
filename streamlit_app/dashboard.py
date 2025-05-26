import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ---------------- FUNGSI ----------------
API_BASE = "https://data-crypto.up.railway.app/api"

def line_chart_compare(df):
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    df['price_normalized'] = df.groupby('symbol')['price_usd'].transform(
        lambda x: (x / x.iloc[0]) * 100
    )
    fig = px.line(
        df, x='scraped_at', y='price_normalized', color='symbol',
        title='📈 Perbandingan Kinerja Aset Kripto (30 Hari)',
        labels={'scraped_at': 'Tanggal', 'price_normalized': 'Kinerja (%)'},
        hover_data={'symbol': True, 'price_normalized': ':.2f', 'scraped_at': '|%d %b %Y'}
    )
    fig.update_layout(xaxis_tickformat="%d %b", xaxis_tickangle=-45, hovermode='x unified')
    return fig

def get_return_df(df):
    latest = df.sort_values('scraped_at').groupby('symbol').last().reset_index()
    first = df.sort_values('scraped_at').groupby('symbol').first().reset_index()
    merged = pd.merge(first[['symbol', 'price_usd']], latest[['symbol', 'price_usd']],
                      on='symbol', suffixes=('_first', '_last'))
    merged['return (%)'] = ((merged['price_usd_last'] / merged['price_usd_first']) - 1) * 100
    merged['return (%)'] = merged['return (%)'].round(2)
    return merged[['symbol', 'return (%)']]

def plot_top_gainers_losers(df_return):
    fig = px.bar(
        df_return.sort_values('return (%)'),
        x='return (%)', y='symbol', orientation='h',
        title="📊 Top Gainers & Losers (30 Hari)",
        color='return (%)',
        color_continuous_scale=['red', 'lightgray', 'green'],
        labels={'return (%)': 'Return (%)', 'symbol': 'Aset'}
    )
    fig.update_layout(xaxis_title="Return (%)", yaxis_title="Symbol", coloraxis_showscale=False)
    return fig

def fetch_history(symbol):
    res = requests.get(f"{API_BASE}/history/{symbol}")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        df['symbol'] = symbol
        return df
    return pd.DataFrame()

# ---------------- HALAMAN ----------------

st.set_page_config(page_title="Crypto Insight", layout="wide")
st.title("📊 Crypto Dashboard (30 Hari Terakhir)")

tab1, tab2 = st.tabs(["📈 Perbandingan Kinerja", "📊 Top Gainers & Losers"])

# ====================== TAB 1 ======================
with tab1:
    try:
        res = requests.get(f"{API_BASE}/symbols")
        symbols_all = sorted(res.json().get("symbols", []))
    except Exception as e:
        st.error(f"❌ Gagal ambil daftar simbol: {e}")
        st.stop()

    selected = st.multiselect("Pilih aset untuk dibandingkan:", symbols_all, default=symbols_all[:2])
    df_compare = pd.DataFrame()

    for sym in selected:
        df = fetch_history(sym)
        if not df.empty:
            df_compare = pd.concat([df_compare, df], ignore_index=True)

    if not df_compare.empty:
        st.plotly_chart(line_chart_compare(df_compare), use_container_width=True)
    else:
        st.warning("Tidak ada data untuk aset yang dipilih.")

# ====================== TAB 2 ======================
with tab2:
    try:
        res = requests.get(f"{API_BASE}/history/all")
        if res.status_code == 200:
            df_all = pd.DataFrame(res.json())
        else:
            st.warning("Gagal ambil semua data historis.")
            df_all = pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Gagal konek ke API: {e}")
        df_all = pd.DataFrame()

    if df_all.empty:
        st.warning("Tidak dapat memuat data aset.")
    else:
        df_all['scraped_at'] = pd.to_datetime(df_all['scraped_at'])
        df_return = get_return_df(df_all)

        # Tampilkan hanya 5 top gainers & 5 losers
        top_n = 3
        df_top = pd.concat([
            df_return.sort_values('return (%)', ascending=False).head(top_n),
            df_return.sort_values('return (%)', ascending=True).head(top_n)
        ])

        st.plotly_chart(plot_top_gainers_losers(df_top), use_container_width=True)
        st.dataframe(df_top.sort_values('return (%)', ascending=False), use_container_width=True)

