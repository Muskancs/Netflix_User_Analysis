# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv('netflix_cleaned_titles.csv')

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=list(df['type'].unique()))
selected_country = st.sidebar.multiselect("Select Country", df['country'].unique(), default=["India", "United States"])
selected_year = st.sidebar.slider("Select Year Added", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2025))

# Filter Data
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['country'].isin(selected_country)) &
    (df['year_added'].between(*selected_year))
]

# Dashboard Title
st.title("🎬 Netflix Dashboard - Timmy x Sentinel Style")

# Summary Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", filtered_df[filtered_df['type'] == 'Movie'].shape[0])
col3.metric("TV Shows", filtered_df[filtered_df['type'] == 'TV Show'].shape[0])

# 📈 Content by Year
st.subheader("📅 Titles Added per Year")
year_counts = filtered_df['year_added'].value_counts().sort_index()
fig_year = px.bar(x=year_counts.index, y=year_counts.values, labels={'x': 'Year', 'y': 'Number of Titles'}, template='plotly_dark')
st.plotly_chart(fig_year, use_container_width=True)

# 🌍 Content by Country
st.subheader("🌍 Top Countries by Content")
top_countries = filtered_df['country'].value_counts().head(10)
fig_country = px.bar(x=top_countries.index, y=top_countries.values, labels={'x': 'Country', 'y': 'Count'}, template='plotly_dark')
st.plotly_chart(fig_country, use_container_width=True)

# 🎭 Genre Cloud
st.subheader("🎭 Top Genres")
genre_series = filtered_df['genres'].dropna().str.split(', ').explode()
top_genres = genre_series.value_counts().head(10)
fig_genres = px.pie(values=top_genres.values, names=top_genres.index, template='plotly_dark', title='Top Genres')
st.plotly_chart(fig_genres, use_container_width=True)
