import requests
import pandas as pd
import folium
from config import AVIATION_STACK_API_KEY
from datetime import datetime

# Fetch flight data
def get_flights(direction: str, iata: str):
    """Fetch flights by direction (arr/dep) and airport code, include all regardless of live data."""
    allowed_airlines = ['Delta Air Lines', 'United Airlines', 'American Airlines', 'Allegiant Air', 'Spirit Airlines']
    
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        f'{direction}_iata': iata,
    }
    response = requests.get('https://api.aviationstack.com/v1/flights', params=params)
    data = response.json().get('data', [])
    # print(response.status_code)
    # print(response)

    flights = []
    for flight in data:
        airline_name = flight['airline']['name']
        if airline_name not in allowed_airlines:
            continue  # skip airlines not in the list
        flights.append({
            'Direction': 'Arrival' if direction == 'arr' else 'Departure',
            'Airline': airline_name,
            'Flight': flight['flight']['iata'],
            'From': flight['departure']['iata'],
            'To': flight['arrival']['iata'],
            'Latitude': flight.get('live', {}).get('latitude') if flight.get('live') else None,
            'Longitude': flight.get('live', {}).get('longitude') if flight.get('live') else None,
            'Altitude (ft)': flight.get('live', {}).get('altitude') if flight.get('live') else None,
            'Speed (km/h)': flight.get('live', {}).get('speed_horizontal') if flight.get('live') else None,
            'Scheduled Departure': flight['departure'].get('scheduled'),
            'Estimated Departure': flight['departure'].get('estimated'),
            'Actual Departure': flight['departure'].get('actual'),
            'Scheduled Arrival': flight['arrival'].get('scheduled'),
            'Estimated Arrival': flight['arrival'].get('estimated'),
            'Actual Arrival': flight['arrival'].get('actual'),
            'Flight Status': flight.get('flight_status')
        })


    return flights


# Fetch arrivals and departures for CHA
arrivals = get_flights('arr', 'CHA')
departures = get_flights('dep', 'CHA')


# Combine and convert to DataFrame
all_flights = arrivals + departures
df = pd.DataFrame(all_flights)

df.columns = [
    'Direction',
    'Airline',
    'Flight',
    'From',
    'To',
    'Latitude',
    'Longitude',
    'Altitude (ft)',
    'Speed (km/h)',
    'Scheduled Departure',
    'Estimated Departure',
    'Actual Departure',
    'Scheduled Arrival',
    'Estimated Arrival',
    'Actual Arrival',
    'Flight Status'
]


datetime_cols = [
    'Scheduled Departure', 'Estimated Departure', 'Actual Departure',
    'Scheduled Arrival', 'Estimated Arrival', 'Actual Arrival'
]

for col in datetime_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')  # convert to datetime, invalid to NaT
    df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M')    # format datetime as string

df[datetime_cols] = df[datetime_cols].fillna('')


# Filter out flights without live data
df = df[(df['Latitude'].notnull()) & (df['Longitude'].notnull())]

if df.empty:
    print("No flights arriving or departing from CHA right now.")
else:
    print("\n🛫🛬 Flights Involving CHA:\n")
    print(df.to_string(index=False))
    # print(df)
