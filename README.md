# Python-Web-App-for-Airline-Booking-Market-Demand-Data
# ✈️ Airline Booking Demand Dashboard

A Python-based web application that analyzes and visualizes airline market demand trends using live flight data from the OpenSky Network API and generates AI-powered business insights via the Groq API (LLaMA 3).

---

## 🔧 Features

### ✅ Real-Time Flight Data via OpenSky
- Fetches recent **arrivals** for selected Australian airports (ICAO: YPAD, YSSY, YMML, YBBN)
- Time-based filter for fetching flights from the last X hours

### ✅ AI-Powered Market Insights (Groq)
- Generates intelligent summaries like:
  - Popular routes
  - Peak travel times
  - Hostel expansion recommendations

### ✅ Clean Interactive Interface
- Built with **Streamlit**
- Filter options and dropdowns in the sidebar
- Dynamic charts with **Plotly**
- Tabular views of raw flight data and popular routes

---

## 🛠 Tech Stack

| Layer            | Tech                                |
|------------------|--------------------------------------|
| Frontend         | Streamlit + Plotly                  |
| Backend/API      | Python, OpenSky API, Groq API       |
| AI Model         | LLaMA 3 via Groq                    |
| Environment Vars | `python-dotenv` for managing secrets|


