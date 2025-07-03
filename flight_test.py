import requests
from config import AVIATION_STACK_API_KEY

params = {
    'access_key': AVIATION_STACK_API_KEY,
    'arr_iata': 'ATL',
    'flight_status': 'active'
}

resp = requests.get('https://api.aviationstack.com/v1/flights', params=params)
data = resp.json()

print(data)
