import streamlit as st
import pytz
from datetime import datetime
import time
from collections import OrderedDict

# --- Configuration de la Page Streamlit ---
# Doit être la première commande Streamlit
st.set_page_config(
    page_title="SMART Market Clock",
    page_icon="🕰️",
    layout="wide"
)

# --- Configuration des Fuseaux Horaires ---

# Rangée 1 : Marchés Mondiaux (Ordonnés d'Ouest en Est)
global_markets = OrderedDict([
    ('New York', 'America/New_York'),
    ('Toronto', 'America/Toronto'),
    ('Londres', 'Europe/London'),
    ('Francfort', 'Europe/Berlin'),
    ('Hong Kong', 'Asia/Hong_Kong'),
    ('Tokyo', 'Asia/Tokyo'),
    ('Sydney', 'Australia/Sydney')
])

# Rangée 2 : Fuseaux Horaires Canadiens (Ordonnés d'Ouest en Est)
canadian_cities = OrderedDict([
    ('Vancouver', 'America/Vancouver'),
    ('Edmonton', 'America/Edmonton'),
    ('Regina', 'America/Regina'),
    ('Winnipeg', 'America/Winnipeg'),
    ('Montréal', 'America/Toronto'),
    ('Moncton', 'America/Moncton'),
    ("St. John's", 'America/St_Johns')
])

# --- Interface Utilisateur ---

st.title("🕰️ SMART Market Clock")

# Créer un emplacement réservé pour l'horloge UTC
utc_placeholder = st.empty()

# Créer des colonnes pour les marchés mondiaux
st.subheader("Marchés Mondiaux")
global_cols = st.columns(len(global_markets))

# Créer des colonnes pour les villes canadiennes
st.subheader("Fuseaux Horaires Canadiens")
canadian_cols = st.columns(len(canadian_cities))


def create_clock_card(city, local_now, show_market_status=False):
    """Génère les informations pour une seule carte d'horloge."""
    
    utc_offset_str = local_now.strftime('%z')
    utc_offset_formatted = f"UTC {utc_offset_str[:3]}:{utc_offset_str[3:]}"
    
    status_text = ""
    status_color = "gray"
    if show_market_status:
        hours = {'Tokyo': (9, 15), 'Hong Kong': (9, 15), 'Sydney': (10, 16), 'Francfort': (9, 18), 'Londres': (8, 17), 'New York': (9, 16), 'Toronto': (9, 16)}
        open_hour, close_hour = hours.get(city, (9, 17))
        
        if open_hour <= local_now.hour < close_hour and local_now.weekday() < 5:
            status_text = '🟢 Ouvert'
        else:
            status_text = '🔴 Fermé'
            
    return f"""
        **{city}**\n
        {local_now.strftime('%Y-%m-%d')}\n
        ## {local_now.strftime('%H:%M')}\n
        <small>{utc_offset_formatted}</small>\n
        {status_text}
    """

# --- Boucle Principale ---
while True:
    utc_now = datetime.now(pytz.utc)

    # Mettre à jour l'horloge UTC
    with utc_placeholder.container():
        st.header(f"{utc_now.strftime('%Y-%m-%d')} - {utc_now.strftime('%H:%M:%S')} UTC")

    # Mettre à jour les horloges mondiales
    for col, (city, tz_name) in zip(global_cols, global_markets.items()):
        with col:
            local_now = utc_now.astimezone(pytz.timezone(tz_name))
            st.markdown(create_clock_card(city, local_now, show_market_status=True), unsafe_allow_html=True)

    # Mettre à jour les horloges canadiennes
    for col, (city, tz_name) in zip(canadian_cols, canadian_cities.items()):
        with col:
            local_now = utc_now.astimezone(pytz.timezone(tz_name))
            st.markdown(create_clock_card(city, local_now), unsafe_allow_html=True)
            
    # Attendre avant la prochaine mise à jour
    time.sleep(1)
