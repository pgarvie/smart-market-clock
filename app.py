import streamlit as st
import pytz
from datetime import datetime
import time
from collections import OrderedDict

# --- Configuration de la Page Streamlit ---
st.set_page_config(
    page_title="SMART Market Clock",
    page_icon="🕰️",
    layout="wide"
)

# --- Configuration des Fuseaux Horaires ---

global_markets = OrderedDict([
    ('New York', 'America/New_York'),
    ('Toronto', 'America/Toronto'),
    ('Londres', 'Europe/London'),
    ('Francfort', 'Europe/Berlin'),
    ('Hong Kong', 'Asia/Hong_Kong'),
    ('Tokyo', 'Asia/Tokyo'),
    ('Sydney', 'Australia/Sydney')
])

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

# Créer un emplacement réservé unique pour toute la page
placeholder = st.empty()

# --- Boucle Principale ---
while True:
    with placeholder.container():
        utc_now = datetime.now(pytz.utc)

        # Affichage de l'horloge UTC
        st.header(f"{utc_now.strftime('%Y-%m-%d')} - {utc_now.strftime('%H:%M:%S')} UTC")
        st.divider()

        # --- Affichage des Marchés Mondiaux ---
        st.subheader("Marchés Mondiaux")
        global_cols = st.columns(len(global_markets))

        for col, (city, tz_name) in zip(global_cols, global_markets.items()):
            local_now = utc_now.astimezone(pytz.timezone(tz_name))
            
            # Calcul du décalage UTC
            utc_offset_str = local_now.strftime('%z')
            utc_offset_formatted = f"UTC {utc_offset_str[:3]}:{utc_offset_str[3:]}"

            # Calcul du statut du marché
            hours = {'Tokyo': (9, 15), 'Hong Kong': (9, 15), 'Sydney': (10, 16), 'Francfort': (9, 18), 'Londres': (8, 17), 'New York': (9, 16), 'Toronto': (9, 16)}
            open_hour, close_hour = hours.get(city, (9, 17))
            is_open = open_hour <= local_now.hour < close_hour and local_now.weekday() < 5
            status_emoji = '🟢' if is_open else '🔴'
            
            # Afficher les informations dans la colonne
            col.metric(
                label=f"{city} ({local_now.strftime('%Y-%m-%d')})",
                value=local_now.strftime('%H:%M'),
                delta=status_emoji
            )
            col.write(f"_{utc_offset_formatted}_")


        st.divider()

        # --- Affichage des Villes Canadiennes ---
        st.subheader("Fuseaux Horaires Canadiens")
        canadian_cols = st.columns(len(canadian_cities))
        
        for col, (city, tz_name) in zip(canadian_cols, canadian_cities.items()):
            local_now = utc_now.astimezone(pytz.timezone(tz_name))
            
            utc_offset_str = local_now.strftime('%z')
            utc_offset_formatted = f"UTC {utc_offset_str[:3]}:{utc_offset_str[3:]}"
            
            col.metric(
                label=f"{city} ({local_now.strftime('%Y-%m-%d')})",
                value=local_now.strftime('%H:%M')
            )
            col.write(f"_{utc_offset_formatted}_")

    # Attendre avant la prochaine mise à jour
    time.sleep(1)
