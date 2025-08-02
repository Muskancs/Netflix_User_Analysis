# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('netflix_cleaned_titles.csv')

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_type = st.sidebar.multiselect("Select Type", df['type'].dropna().unique(), default=list(df['type'].dropna().unique()))
selected_country = st.sidebar.multiselect("Select Country", df['country'].dropna().unique(), default=["India", "United States"])
selected_year = st.sidebar.slider("Select Year Added", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2025))

# Filter Data
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['country'].isin(selected_country)) &
    (df['year_added'].between(*selected_year))
]

# Title
st.title("🎬 Netflix Dashboard - Timmy x Sentinel")

# Summary Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", filtered_df[filtered_df['type'] == 'Movie'].shape[0])
col3.metric("TV Shows", filtered_df[filtered_df['type'] == 'TV Show'].shape[0])

# 📅 Titles per Year
st.subheader("📅 Titles Added per Year")
year_counts = filtered_df['year_added'].value_counts().sort_index()
fig_year = px.bar(x=year_counts.index, y=year_counts.values, labels={'x': 'Year', 'y': 'Titles'}, template='plotly_dark')
st.plotly_chart(fig_year, use_container_width=True)

# 🌍 Top Countries
st.subheader("🌍 Top Countries by Titles")
top_countries = filtered_df['country'].value_counts().head(10)
fig_country = px.bar(x=top_countries.index, y=top_countries.values, labels={'x': 'Country', 'y': 'Count'}, template='plotly_dark')
st.plotly_chart(fig_country, use_container_width=True)

# 🎭 Genre Pie Chart
st.subheader("🎭 Top Genres")
genre_series = filtered_df['genres'].dropna().str.split(', ').explode()
top_genres = genre_series.value_counts().head(10)
fig_genres = px.pie(values=top_genres.values, names=top_genres.index, title="Top Genres", template='plotly_dark')
st.plotly_chart(fig_genres, use_container_width=True)

# 🎬 Top Directors
st.subheader("🎬 Top Directors")
top_directors = filtered_df['director'].dropna().str.split(', ').explode().value_counts().head(10)
fig_directors = px.bar(x=top_directors.index, y=top_directors.values, labels={'x': 'Director', 'y': 'Count'}, template='plotly_dark')
st.plotly_chart(fig_directors, use_container_width=True)

# 🎭 Top Actors
st.subheader("🎭 Top Actors")
top_actors = filtered_df['cast'].dropna().str.split(', ').explode().value_counts().head(10)
fig_actors = px.bar(x=top_actors.index, y=top_actors.values, labels={'x': 'Actor', 'y': 'Appearances'}, template='plotly_dark')
st.plotly_chart(fig_actors, use_container_width=True)

# 🏷 Content Ratings Distribution
st.subheader("🏷 Content Rating Distribution")
fig_ratings = px.histogram(filtered_df, x='rating', color='type', barmode='group', template='plotly_dark')
st.plotly_chart(fig_ratings, use_container_width=True)

# 📈 Average Vote by Release Year
st.subheader("📈 Average Vote per Release Year")
avg_votes = filtered_df.groupby('release_year')['vote_average'].mean().dropna()
fig_avg_vote = px.line(x=avg_votes.index, y=avg_votes.values, labels={'x': 'Year', 'y': 'Avg Vote'}, template='plotly_dark')
st.plotly_chart(fig_avg_vote, use_container_width=True)

# 💸 Budget vs Revenue
st.subheader("💸 Budget vs Revenue (Movies only)")
movies = filtered_df[(filtered_df['type'] == 'Movie') & filtered_df['budget'].notnull() & filtered_df['revenue'].notnull()]
fig_budget = px.scatter(movies, x='budget', y='revenue', size='popularity', color='rating',
                        hover_data=['title'], template='plotly_dark', title="Budget vs Revenue")
st.plotly_chart(fig_budget, use_container_width=True)
