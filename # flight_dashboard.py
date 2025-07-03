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

# Refresh button
if st.button("🔄 Refresh Flight Data"):
    st.experimental_rerun()

# Fetch flight data
def get_flights(direction: str, iata: str):
    """Fetch flights by direction (arr/dep) and airport code, include all regardless of live data."""
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        f'{direction}_iata': iata,
    }
    response = requests.get('https://api.aviationstack.com/v1/flights', params=params)
    data = response.json().get('data', [])
    # print(response)  # HTTP status code

    flights = []
    for flight in data:
        flights.append({
            'Direction': 'Arrival' if direction == 'arr' else 'Departure',
            'Airline': flight['airline']['name'],
            'Flight': flight['flight']['iata'],
            'From': flight['departure']['iata'],
            'To': flight['arrival']['iata'],
            'Latitude': flight.get('live', {}).get('latitude') if flight.get('live') else None,
            'Longitude': flight.get('live', {}).get('longitude') if flight.get('live') else None,
            'Altitude (ft)': flight.get('live', {}).get('altitude') if flight.get('live') else None,
            'Speed (km/h)': flight.get('live', {}).get('speed_horizontal') if flight.get('live') else None
        })

    return flights


# Fetch arrivals and departures for CHA
arrivals = get_flights('arr', 'CHA')
departures = get_flights('dep', 'CHA')


# Combine and convert to DataFrame
all_flights = arrivals + departures
df = pd.DataFrame(all_flights)
# df.columns
df.columns = ['Direction', 'Airline', 'Flight', 'From', 'To', 'Latitude', 'Longitude', 'Altitude (ft)', 'Speed (km/h)']
# Filter out flights without live data
df = df[(df['Latitude'].notnull()) & (df['Longitude'].notnull())]

# Show results
if df.empty:
    st.warning("No live flights arriving or departing from CHA.")
else:
    st.dataframe(df)
    
    # Map
    m = folium.Map(location=MAP_CENTER, zoom_start=6)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Flight']} ({row['Airline']})\n{row['From']} ➜ {row['To']}",
            tooltip=row['Direction'],
            icon=folium.Icon(color='blue' if row['Direction'] == 'Arrival' else 'green')
        ).add_to(m)

    st.markdown("### 📍 Live Flight Map")
    st_folium(m, width=700, height=500)

    # Timestamp
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
