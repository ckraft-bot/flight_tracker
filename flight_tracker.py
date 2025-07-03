import requests
import pandas as pd
import folium
from config import AVIATION_STACK_API_KEY

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
df.columns
df.columns = ['Direction', 'Airline', 'Flight', 'From', 'To', 'Latitude', 'Longitude', 'Altitude (ft)', 'Speed (km/h)']
# Filter out flights without live data
df = df[(df['Latitude'].notnull()) & (df['Longitude'].notnull())]

if df.empty:
    print("No flights arriving or departing from CHA right now.")
else:
    print("\n🛫🛬 Flights Involving CHA:\n")
    print(df.to_string(index=False))

# Display map
# if not df.empty:
#     # Create a Folium map centered roughly at CHA airport coordinates
#     cha_lat, cha_lon = 35.0442, -85.2017  # CHA coordinates
    
#     flight_map = folium.Map(location=[cha_lat, cha_lon], zoom_start=7, tiles='CartoDB positron')

#     # Add markers for each flight
#     for _, row in df.iterrows():
#         popup_text = (
#             f"{row['Direction']} - {row['Airline']} {row['Flight']}<br>"
#             f"From: {row['From']}<br>"
#             f"To: {row['To']}<br>"
#             f"Altitude: {row['Altitude (ft)']} ft<br>"
#             f"Speed: {row['Speed (km/h)']} km/h"
#         )
#         folium.CircleMarker(
#             location=[row['Latitude'], row['Longitude']],
#             radius=6,
#             popup=popup_text,
#             color='blue' if row['Direction'] == 'Arrival' else 'red',
#             fill=True,
#             fill_opacity=0.7
#         ).add_to(flight_map)

#     # Save the map to an HTML file and print its path
#     flight_map.save('cha_flights_map.html')
#     print("\nMap saved as 'cha_flights_map.html'. Open this file in your browser to see live flight locations.")
