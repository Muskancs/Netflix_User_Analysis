import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Set page configuration
st.set_page_config(page_title="🎬 Netflix Dashboard", layout="wide")

# Sidebar: Theme selector
theme_choice = st.sidebar.radio("🎨 Choose Theme", ["Light", "Dark"])

# Apply theme using custom CSS
def apply_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
            body {
                background-color: #0e1117;
                color: #ffffff;
            }
            .css-1d391kg, .stApp {
                background-color: #0e1117 !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            body {
                background-color: #ffffff;
                color: #000000;
            }
            .css-1d391kg, .stApp {
                background-color: #ffffff !important;
                color: black !important;
            }
            </style>
        """, unsafe_allow_html=True)

apply_theme(theme_choice)

# Load Data
df = pd.read_csv('netflix_cleaned_titles.csv')

# Add a year column
df['year_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year

# Summary Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("📦 Total Titles", df.shape[0])
col2.metric("🎥 Movies", df[df['type'] == 'Movie'].shape[0])
col3.metric("📺 TV Shows", df[df['type'] == 'TV Show'].shape[0])
col4.metric("📅 Active Years", f"{df['release_year'].min()} - {df['release_year'].max()}")

st.markdown("---")

# Filter sidebar
countries = df['country'].dropna().unique().tolist()
selected_country = st.sidebar.selectbox("🌍 Filter by Country", sorted(countries), index=0)

filtered_df = df[df['country'] == selected_country]

# Section: Top Genres by Country
st.subheader(f"🎭 Genre Distribution in {selected_country}")
genre_data = filtered_df['listed_in'].dropna().str.split(',').explode().str.strip()
top_genres = genre_data.value_counts().head(10)

fig1, ax1 = plt.subplots()
sns.barplot(x=top_genres.values, y=top_genres.index, palette='Set2', ax=ax1)
ax1.set_title("Top Genres")
st.pyplot(fig1)

# Section: Trend Over Years
st.subheader(f"📈 Titles Added Over Time in {selected_country}")
year_counts = filtered_df['year_added'].value_counts().sort_index()
fig2 = px.line(x=year_counts.index, y=year_counts.values,
               labels={"x": "Year", "y": "Number of Titles"},
               title="Content Added Over Time")
st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Built by Muskan | Timmy x Deepfake Sentinel Project 🚀")
