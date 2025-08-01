import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('netflix_titles.csv')

# Preprocessing
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df = df.dropna(subset=['date_added'])

st.set_page_config(layout="wide")
st.title("🎬 Netflix User Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("📊 Filter Content")
content_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=list(df['type'].unique()))
years = st.sidebar.slider("Select Year Range", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2020))
country = st.sidebar.selectbox("Select Country", ['All'] + sorted(df['country'].dropna().unique().tolist()))

# Apply Filters
filtered_df = df[df['type'].isin(content_type)]
filtered_df = filtered_df[(filtered_df['year_added'] >= years[0]) & (filtered_df['year_added'] <= years[1])]
if country != 'All':
    filtered_df = filtered_df[filtered_df['country'].str.contains(country)]

st.markdown("### 📈 Content Type Distribution")
st.bar_chart(filtered_df['type'].value_counts())

st.markdown("### 📅 Yearly Content Added")
year_data = filtered_df['year_added'].value_counts().sort_index()
st.line_chart(year_data)

st.markdown("### 🌍 Top Countries by Content")
top_countries = df['country'].dropna().str.split(', ').explode().value_counts().head(10)
st.bar_chart(top_countries)

st.markdown("### 🎭 Genre Word Cloud")
st.image("genre_wordcloud.png", use_column_width=True)

st.markdown("### 🤖 Clustering of Content (NLP)")
st.image("genre_clusters.png", use_column_width=True)

st.markdown("---")
st.markdown("Built with ❤️ by Muskan Bisht")
