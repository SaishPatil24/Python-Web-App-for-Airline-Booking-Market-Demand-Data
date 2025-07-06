import streamlit as st
from dotenv import load_dotenv
from core.opensky_data import fetch_flights
from core.analytics import process_flight_data, get_popular_routes
from core.ai_summary import generate_ai_summary
from ui.components import sidebar_controls, show_data_section
import datetime

load_dotenv()

st.set_page_config(page_title="Airline Booking Demand Dashboard", layout="wide")
st.title("🛩️ Airline Booking Demand Dashboard")

# Sidebar Filters
airport, hours_back = sidebar_controls()

# Add airport code validation
st.info(f"📍 Searching for flights at airport: **{airport}** (last {hours_back} hours)")

# Main
with st.spinner("Fetching flight data..."):
    now = datetime.datetime.utcnow()
    begin = int((now - datetime.timedelta(hours=hours_back)).timestamp())
    end = int(now.timestamp())
    
    # Show debug info
    st.write(f"🕐 Time range: {datetime.datetime.fromtimestamp(begin)} to {datetime.datetime.fromtimestamp(end)}")
    
    flights = fetch_flights(airport, begin, end)

# Better error handling
if flights is None:
    st.error("❌ Failed to fetch flight data from OpenSky API")
    st.write("**Possible solutions:**")
    st.write("1. Check if airport code is correct (use ICAO format like KJFK, EGLL)")
    st.write("2. Try a different time period (some airports may have limited data)")
    st.write("3. Try a major international airport")
    
    # Suggest popular airport codes
    st.write("**Popular airport codes to try:**")
    st.write("- KJFK (New York JFK)")
    st.write("- EGLL (London Heathrow)")
    st.write("- KLAX (Los Angeles)")
    st.write("- LFPG (Paris Charles de Gaulle)")
    st.write("- EDDF (Frankfurt)")
    
    # Option to use sample data
    if st.button("🧪 Use Sample Data for Testing"):
        sample_flights = [
            {
                "icao24": "abc123",
                "callsign": "UAL123",
                "estDepartureAirport": airport,
                "estArrivalAirport": "EGLL",
                "firstSeen": int((now - datetime.timedelta(hours=2)).timestamp()),
                "lastSeen": int((now - datetime.timedelta(hours=1)).timestamp())
            },
            {
                "icao24": "def456", 
                "callsign": "BAW456",
                "estDepartureAirport": airport,
                "estArrivalAirport": "KJFK",
                "firstSeen": int((now - datetime.timedelta(hours=3)).timestamp()),
                "lastSeen": int((now - datetime.timedelta(hours=2)).timestamp())
            }
        ]
        flights = sample_flights
        st.success("✅ Using sample data for demonstration")
    else:
        st.stop()

elif len(flights) == 0:
    st.warning(f"⚠️ No flight data found for {airport} in the last {hours_back} hours")
    st.write("**Try:**")
    st.write("- Increasing the time period")
    st.write("- Using a busier airport")
    st.write("- Checking if the airport code is correct")
    st.stop()

else:
    st.success(f"✅ Found {len(flights)} flights for {airport}")

# Process Data
df = process_flight_data(flights)
popular_routes = get_popular_routes(df)

# Show Tables & Charts
show_data_section(df, popular_routes)

# AI Market Summary
with st.expander("🤖 AI-Generated Market Insights"):
    with st.spinner("Generating AI insights..."):
        insight = generate_ai_summary(df, airport, hours_back)
        st.markdown(insight)