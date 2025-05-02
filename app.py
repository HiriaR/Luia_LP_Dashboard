
import streamlit as st
import requests
import datetime

# Paramètres utilisateur
MY_POOL_SHARE = 0.0237447669  # 2.374 %
MY_TOTAL_LP_USD = 1331.07
LUIA_DECIMALS = 0.00017025  # prix en euros ou dollars approximatif

# Fonctions API
@st.cache_data(ttl=300)
def get_luia_price():
    url = "https://api.geckoterminal.com/api/v2/networks/bsc/pools/0x2200c5ac2f9d8d635db040a6f4eab5ef6bf9e855"
    r = requests.get(url)
    data = r.json()
    try:
        price = float(data['data']['attributes']['base_token_price_usd'])
    except:
        price = LUIA_DECIMALS
    return price

@st.cache_data(ttl=300)
def get_24h_volume():
    url = "https://api.geckoterminal.com/api/v2/networks/bsc/pools/0x2200c5ac2f9d8d635db040a6f4eab5ef6bf9e855"
    r = requests.get(url)
    data = r.json()
    try:
        volume = float(data['data']['attributes']['volume_usd']['h24'])
    except:
        volume = 0.0
    return volume

# Interface
st.set_page_config(page_title="LUIA/WBNB LP Dashboard", layout="wide")
st.title("LUIA / WBNB LP Tracker")
st.markdown("Suivi en temps réel de vos gains en fourniture de liquidité")

col1, col2, col3 = st.columns(3)

with col1:
    price = get_luia_price()
    st.metric("Prix actuel du LUIA", f"{price:.8f} $")

with col2:
    volume_24h = get_24h_volume()
    st.metric("Volume sur 24h", f"{volume_24h:,.2f} $")

with col3:
    estimated_fees = volume_24h * 0.0017 * MY_POOL_SHARE  # 0.17% fees * pool share
    luia_gains = estimated_fees / price
    st.metric("Gains estimés aujourd'hui", f"{estimated_fees:.2f} $ ({luia_gains:,.0f} LUIA)")

st.divider()

st.subheader("Détails LP")
st.write(f"**Part du pool :** {MY_POOL_SHARE * 100:.4f}%")
st.write(f"**Valeur de votre LP :** {MY_TOTAL_LP_USD:,.2f} $")
st.write(f"**Estimation valeur LP en LUIA :** {MY_TOTAL_LP_USD / price:,.0f} LUIA")

st.caption("Dashboard créé pour Hiria par Jarvis. Données GeckoTerminal | Actualisé toutes les 5 minutes.")

