import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from config import AVIATION_STACK_API_KEY
from datetime import datetime

# Must be first
st.set_page_config(page_title="Local Flight Dashboard", layout="wide")
st.title("🛫🛬 Local Flight Dashboard")

# Constants
DEFAULT_IATA = "CHA"
MAP_CENTER = [35.035, -85.203]
ALLOWED_AIRLINES = ['Delta Air Lines', 'United Airlines', 'American Airlines', 'Allegiant Air', 'Spirit Airlines']

# Refresh button
if st.button("🔄 Refresh Flight Data"):
    st.rerun()

# Flight data fetcher
def get_flights(direction: str, iata: str):
    """Fetch flights by direction (arr/dep) and airport code, filter by allowed airlines."""
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        f'{direction}_iata': iata,
    }
    response = requests.get('https://api.aviationstack.com/v1/flights', params=params)
    data = response.json().get('data', [])

    flights = []
    for flight in data:
        airline_name = flight['airline']['name']
        if airline_name not in ALLOWED_AIRLINES:
            continue

        departure = flight.get('departure') or {}
        arrival = flight.get('arrival') or {}
        live = flight.get('live') or {}

        flights.append({
            'Direction': 'Arrival' if direction == 'arr' else 'Departure',
            'Airline': airline_name,
            'Flight': flight['flight']['iata'],
            'From': departure.get('iata'),
            'To': arrival.get('iata'),
            'Latitude': live.get('latitude'),
            'Longitude': live.get('longitude'),
            'Altitude (ft)': live.get('altitude'),
            'Speed (km/h)': live.get('speed_horizontal'),
            'Scheduled Departure': departure.get('scheduled'),
            'Estimated Departure': departure.get('estimated'),
            'Actual Departure': departure.get('actual'),
            'Scheduled Arrival': arrival.get('scheduled'),
            'Estimated Arrival': arrival.get('estimated'),
            'Actual Arrival': arrival.get('actual'),
            'Flight Status': flight.get('flight_status')
        })

    return flights

# Get and combine flights
arrivals = get_flights('arr', DEFAULT_IATA)
departures = get_flights('dep', DEFAULT_IATA)
df = pd.DataFrame(arrivals + departures)

# Format datetime fields
datetime_cols = [
    'Scheduled Departure', 'Estimated Departure', 'Actual Departure',
    'Scheduled Arrival', 'Estimated Arrival', 'Actual Arrival'
]
for col in datetime_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
df[datetime_cols] = df[datetime_cols].fillna('')

# Filter for live flights with coordinates
df = df[df['Latitude'].notnull() & df['Longitude'].notnull()]

# Display table and map
if df.empty:
    st.warning("No live flights arriving or departing from CHA.")
else:
    st.dataframe(df)

    m = folium.Map(location=MAP_CENTER, zoom_start=6)
    for _, row in df.iterrows():
        icon_color = 'yellow' if row['Direction'] == 'Arrival' else 'blue'
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Flight']} ({row['Airline']})\n{row['From']} ➜ {row['To']}",
            tooltip=row['Direction'],
            icon=folium.Icon(icon='plane', prefix='fa', color=icon_color)
        ).add_to(m)

    st.markdown("### 📍 Live Flight Map")
    st_folium(m, width=700, height=500)

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
