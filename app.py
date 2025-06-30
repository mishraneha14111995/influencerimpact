import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("influencer_campaigns.csv")
    return df

df = load_data()
st.set_page_config(layout="wide", page_title="Influencer Campaign Dashboard")

st.title("📊 Influencer Marketing Dashboard")
st.markdown("This dashboard helps you identify which influencer marketing strategies result in the highest monthly sales.")

# Sidebar filters
with st.sidebar:
    st.header("Filter Options")
    platforms = st.multiselect("Select Platform(s)", options=df["platform"].unique(), default=df["platform"].unique())
    content_types = st.multiselect("Select Content Type(s)", options=df["content_type"].unique(), default=df["content_type"].unique())
    min_sales, max_sales = st.slider("Monthly Sales Range", float(df["monthly_sales"].min()), float(df["monthly_sales"].max()), (float(df["monthly_sales"].min()), float(df["monthly_sales"].max())))

# Filter dataset
filtered_df = df[
    (df["platform"].isin(platforms)) &
    (df["content_type"].isin(content_types)) &
    (df["monthly_sales"] >= min_sales) &
    (df["monthly_sales"] <= max_sales)
]

# Tabs for organization
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Strategy Insights", "Engagement Metrics", "Data Table & Summary"])

# --- OVERVIEW TAB ---
with tab1:
    st.subheader("Overview of Campaign Performance")

    st.markdown("📌 **Total Monthly Sales across all selected filters**")
    st.metric("Total Sales (AED)", f"AED {filtered_df['monthly_sales'].sum():,.0f}")

    st.markdown("📌 **Average Engagement Rate per Platform**")
    fig1 = px.bar(filtered_df.groupby("platform")["engagement_rate"].mean().reset_index(), 
                  x="platform", y="engagement_rate", color="platform", title="Avg Engagement Rate by Platform")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("📌 **Distribution of Monthly Sales**")
    fig2 = px.histogram(filtered_df, x="monthly_sales", nbins=30, title="Distribution of Monthly Sales")
    st.plotly_chart(fig2, use_container_width=True)

# --- STRATEGY INSIGHTS TAB ---
with tab2:
    st.subheader("Influencer Strategy Insights")

    st.markdown("📌 **Top 10 Influencers by Sales**")
    top_inf = filtered_df.groupby("influencer_name")["monthly_sales"].sum().sort_values(ascending=False).head(10).reset_index()
    fig3 = px.bar(top_inf, x="influencer_name", y="monthly_sales", title="Top 10 Influencers by Sales")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("📌 **Content Type vs Average Sales**")
    fig4 = px.box(filtered_df, x="content_type", y="monthly_sales", color="content_type", title="Sales by Content Type")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("📌 **Platform vs Sales Relationship**")
    fig5 = px.violin(filtered_df, x="platform", y="monthly_sales", color="platform", box=True, title="Sales by Platform")
    st.plotly_chart(fig5, use_container_width=True)

# --- ENGAGEMENT METRICS TAB ---
with tab3:
    st.subheader("Engagement and Conversion Metrics")

    st.markdown("📌 **Correlation Heatmap**")
    fig, ax = plt.subplots()
    sns.heatmap(filtered_df[["followers", "engagement_rate", "clicks", "impressions", "ad_spend", "monthly_sales"]].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    st.markdown("📌 **Clicks vs Sales**")
    fig6 = px.scatter(filtered_df, x="clicks", y="monthly_sales", trendline="ols", title="Clicks vs Sales")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("📌 **Ad Spend vs Sales**")
    fig7 = px.scatter(filtered_df, x="ad_spend", y="monthly_sales", color="platform", trendline="ols", title="Ad Spend vs Sales")
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("📌 **Impressions vs Clicks**")
    fig8 = px.scatter(filtered_df, x="impressions", y="clicks", color="content_type", trendline="ols", title="Impressions vs Clicks")
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("📌 **Engagement Rate vs Monthly Sales**")
    fig9 = px.scatter(filtered_df, x="engagement_rate", y="monthly_sales", size="followers", color="platform", title="Engagement Rate vs Sales")
    st.plotly_chart(fig9, use_container_width=True)

# --- DATA TABLE TAB ---
with tab4:
    st.subheader("Data Table & Key Summary")

    st.markdown("📌 **Filtered Dataset Table**")
    st.dataframe(filtered_df)

    st.markdown("📌 **Summary Statistics**")
    st.write(filtered_df.describe())

    st.download_button("Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_influencer_data.csv")

st.markdown("---")
st.markdown("✅ *Dashboard created for Director-Sales & Stakeholders to monitor influencer strategy effectiveness.*")
