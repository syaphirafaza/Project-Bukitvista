import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data_rentals_bukitvista.csv")

df = load_data()

# Cleaning the bedroom and bathroom values
def clean_room_info(value):
    try:
        return int(re.search(r'\d+', str(value)).group())
    except:
        return np.nan

df['bedrooms'] = df['bedrooms'].apply(clean_room_info)
df['bathrooms'] = df['bathrooms'].apply(clean_room_info)

# Navigation Tab
tab1, tab2 = st.tabs(["📊 Property EDA : Unlock insights through comprehensive exploratory data analysis.", "🏠 Property Recommendations : Discover the perfect properties tailored to your needs."])

# EDA Tab
with tab1:
    st.subheader("💼 Premium Picks: The 3 Most Exclusive Villas")
    top3_expensive = df[['name', 'price_per_day_usd', 'property_type']].dropna().sort_values(by='price_per_day_usd', ascending=False).head(3)
    st.dataframe(top3_expensive)

    st.subheader("💸 Budget Bliss: Top 3 Most Affordable Villas per Night")
    top3_cheap = df[['name', 'price_per_day_usd', 'property_type']].dropna().sort_values(by='price_per_day_usd', ascending=True).head(3)
    st.dataframe(top3_cheap)

with tab1:
    st.subheader("📈 Property Agency Distribution")

    # Cek apakah kolom agency ada
    if 'agency' in df.columns:
        agency_counts = df['agency'].value_counts()
        st.write("Number of properties per agency:")
        st.dataframe(agency_counts)

        st.subheader("Agency Distribution Visualization")
        fig2, ax2 = plt.subplots()
        agency_counts.plot(kind='bar', color='purple', edgecolor='black', ax=ax2)
        ax2.set_ylabel("Number of Properties")
        ax2.set_xlabel("Agency")
        ax2.set_title("Property Distribution Based on Agency")
        st.pyplot(fig2)

        # Specific analysis for BukitVista
        if 'BukitVista' in df['agency'].str.lower().unique():
            bv_count = df['agency'].str.lower().str.contains("BukitVista").sum()
            st.success(f"✅ Properties Using BukitVista Agency **BukitVista**: {bv_count}")
    else:
        st.error("Column 'agency' not found in data.")


# Recommendations Tab
with tab2:
    st.title("🏠 Rental Property Recommendations : Find the best rental properties that fit your lifestyle.")

    st.sidebar.header("🎯 Your Preferences, Our Filters")
    lokasi_unik = df['location'].dropna().unique()
    if len(lokasi_unik) == 0:
        st.warning("Location data is not yet available.")
    else:
        selected_location = st.sidebar.selectbox("Select Location", sorted(lokasi_unik))
        max_budget = st.sidebar.number_input("Maximum Budget per Night (USD)", min_value=0, value=100)

        rekomendasi_df = df[
            (df['location'] == selected_location) &
            (df['price_per_day_usd'] <= max_budget)
        ]

        st.subheader(f"Properties in {selected_location} with price <= ${max_budget}")
        if not rekomendasi_df.empty:
            st.dataframe(rekomendasi_df[['name', 'location', 'bedrooms', 'bathrooms', 'period_days', 'price_per_day_usd', 'price_per_day_idr']])
        else:
            st.warning("No properties match your criteria.")
