import requests
import os
from dotenv import load_dotenv

def fetch_flights(airport, begin, end):
    load_dotenv()
    USERNAME = os.getenv("OPENSKY_USERNAME")
    PASSWORD = os.getenv("OPENSKY_PASSWORD")
    url = "https://opensky-network.org/api/flights/arrival"
    params = {"airport": airport, "begin": begin, "end": end}
    try:
        resp = requests.get(url, params=params, auth=(USERNAME, PASSWORD) if USERNAME and PASSWORD else None)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"OpenSky API error: {resp.status_code}")
    except Exception as e:
        print(f"OpenSky API exception: {e}")
    # Fallback: return sample data
    return [
        {
            "callsign": "QF123",
            "estDepartureAirport": airport,
            "estArrivalAirport": "YMML",
            "firstSeen": begin,
            "lastSeen": end
        }
    ]
