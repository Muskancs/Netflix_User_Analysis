import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# -------------------------------
# Set Streamlit page config
# -------------------------------
st.set_page_config(page_title="Netflix Data Dashboard", layout="wide")

# -------------------------------
# Load the dataset
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("netflix_movies_detailed_up_to_2025.csv")

df = load_data()

# -------------------------------
# Header
# -------------------------------
st.title("🎬 Netflix Data Analysis Dashboard")
st.markdown("An interactive dashboard to explore Netflix content trends till 2025.")

# -------------------------------
# Key Stats Cards
# -------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Total Titles", df.shape[0])
with col2:
    st.metric("📅 Most Active Year", df['release_year'].value_counts().idxmax())
with col3:
    st.metric("🎭 Unique Genres", df['genres'].nunique())

# -------------------------------
# Content Type Count Plot
# -------------------------------
st.subheader("📊 Content Type Distribution")
fig1, ax1 = plt.subplots()
sns.countplot(data=df, x='type', palette='Set2', ax=ax1)
ax1.set_title("Distribution of Content Types")
st.pyplot(fig1)

# -------------------------------
# Genre WordCloud
# -------------------------------
st.subheader("🌈 Genre Word Cloud")
genre_text = ','.join(df['genres'].dropna().astype(str))
wordcloud = WordCloud(
    width=1000,
    height=400,
    background_color='black',
    colormap='Set2',
    collocations=False
).generate(genre_text)

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.imshow(wordcloud, interpolation='bilinear')
ax2.axis('off')
st.pyplot(fig2)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("👩‍💻 **Created by Muskan Bisht** | 📧 Reach me on [LinkedIn](https://www.linkedin.com/)")

