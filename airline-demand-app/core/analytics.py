import pandas as pd

def process_flight_data(flights):
    records = []
    for f in flights:
        records.append({
            "callsign": f.get("callsign", None),
            "departure": f.get("estDepartureAirport", None),
            "arrival": f.get("estArrivalAirport", None),
            "departure_time": pd.to_datetime(f.get("firstSeen", None), unit="s"),
            "arrival_time": pd.to_datetime(f.get("lastSeen", None), unit="s")
        })
    return pd.DataFrame(records)

def get_popular_routes(df):
    return df.groupby(["departure", "arrival"]).size().reset_index(name="count").sort_values("count", ascending=False)