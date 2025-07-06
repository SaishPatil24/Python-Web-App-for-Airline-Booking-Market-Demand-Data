import streamlit as st
import plotly.express as px

def sidebar_controls():
    st.sidebar.header("Airport & Time Settings")
    airport = st.sidebar.selectbox("Select Airport (ICAO)", ["KLAX", "KJFK", "EGLL", "YSSY", "YPAD"], index=0)

    hours_back = st.sidebar.slider("Hours Back", 1, 6, 3)
    return airport, hours_back

def show_data_section(df, popular_routes):
    st.subheader("📄 Raw Flight Data")
    st.dataframe(df, use_container_width=True)

    st.subheader("🔥 Most Popular Routes")
    st.dataframe(popular_routes, use_container_width=True)

    fig = px.bar(popular_routes.head(10), x="count", y="arrival", color="departure", orientation="h", title="Top Routes")
    st.plotly_chart(fig, use_container_width=True)
