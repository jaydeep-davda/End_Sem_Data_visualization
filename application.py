#Import libraries
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Global Video Game Sales Dashboard",
    layout="wide"
)

#Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_video_game_sales.csv")

df = load_data()

#Sidebar filters
st.sidebar.header("🎛️ Filters")

platforms = sorted(df['console'].unique())

selected_platforms = st.sidebar.multiselect(
    "Select Platform(s)",
    platforms,
    default=platforms[:5]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['year'].min()),
    int(df['year'].max()),
    (1995, 2015)
)

filtered_df = df[
    (df['console'].isin(selected_platforms)) &
    (df['year'].between(year_range[0], year_range[1]))
]

#st.title("🎮 Video Game Sales Dashboard")
st.title("🎮 Global Video Game Sales Dashboard")
st.markdown("Interactive analysis of video game sales across platforms, genres, publishers, and regions.")

#Visualization 1: Global sales over time
sales_by_year = filtered_df.groupby('year')['total_sales'].sum().reset_index()

fig1 = px.line(
    sales_by_year, x='year', y='total_sales',
    title="Global Video Game Sales Over Time",
    labels={'total_sales': 'Sales (Millions)'}
)
st.plotly_chart(fig1, use_container_width=True)

#Visualization 2: Top platforms by sales
platform_sales = (
    filtered_df.groupby('console')['total_sales']
    .sum().sort_values(ascending=False).reset_index()
)

fig2 = px.bar(
    platform_sales, x='console', y='total_sales',
    title="Total Global Sales by Platform"
)
st.plotly_chart(fig2, use_container_width=True)

#Visualization 3: Genre sales distribution
platform_year_sales = (
    filtered_df.groupby(['year', 'console'])['total_sales']
    .sum().reset_index()
)

fig3 = px.line(
    platform_year_sales,
    x='year', y='total_sales', color='console',
    title="Platform Sales Trends Over Time"
)
st.plotly_chart(fig3, use_container_width=True)

#Visualization 4: Top publishers table
genre_sales = (
    filtered_df.groupby('genre')['total_sales']
    .sum().sort_values(ascending=False).reset_index()
)

fig4 = px.bar(
    genre_sales, x='genre', y='total_sales',
    title="Global Sales by Genre"
)
st.plotly_chart(fig4, use_container_width=True)

#Visualization 5: Genre Preferences by Region
region_genre = (
    filtered_df.groupby('genre')[['na_sales', 'pal_sales', 'jp_sales']]
    .sum().reset_index()
)

fig5 = px.bar(
    region_genre,
    x='genre',
    y=['na_sales', 'pal_sales', 'jp_sales'],
    title="Genre Preferences by Region",
    labels={'value': 'Sales (Millions)', 'variable': 'Region'}
)
st.plotly_chart(fig5, use_container_width=True)

#Visualization 6: Distribution of Global Sales
fig6 = px.histogram(
    filtered_df,
    x='total_sales',
    nbins=50,
    title="Distribution of Global Video Game Sales"
)
st.plotly_chart(fig6, use_container_width=True)

#Visualization 7: Top Publishers by Sales
publisher_sales = (
    filtered_df.groupby('publisher')['total_sales']
    .sum().sort_values(ascending=False).head(10).reset_index()
)

fig7 = px.bar(
    publisher_sales,
    x='publisher', y='total_sales',
    title="Top 10 Publishers by Global Sales"
)
st.plotly_chart(fig7, use_container_width=True)

#Visualization 8: Number of Games Released per Year
games_per_year = filtered_df.groupby('year')['title'].count().reset_index()

fig8 = px.line(
    games_per_year,
    x='year', y='title',
    title="Number of Video Games Released per Year",
    labels={'title': 'Number of Games'}
)
st.plotly_chart(fig8, use_container_width=True)

#Visualization 9: Average Sales per Game by Platform
avg_sales_platform = (
    filtered_df.groupby('console')['total_sales']
    .mean().sort_values(ascending=False).head(10).reset_index()
)

fig9 = px.bar(
    avg_sales_platform,
    x='console', y='total_sales',
    title="Average Global Sales per Game (Top Platforms)"
)
st.plotly_chart(fig9, use_container_width=True)

#Visualization 10: Platform Lifespan
platform_lifespan = (
    filtered_df.groupby('console')['year']
    .agg(['min', 'max']).reset_index()
)

platform_lifespan['lifespan'] = platform_lifespan['max'] - platform_lifespan['min']
top_lifespan = platform_lifespan.sort_values('lifespan', ascending=False).head(10)

fig10 = px.bar(
    top_lifespan,
    x='console', y='lifespan',
    title="Platform Lifespan (Years Active)",
    labels={'lifespan': 'Years'}
)
st.plotly_chart(fig10, use_container_width=True)

#interactive data table:
st.subheader("📋 Filtered Dataset Preview")

st.dataframe(filtered_df.head(50))


