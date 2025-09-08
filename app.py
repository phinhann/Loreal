# -*- coding: utf-8 -*-
"""Streamlit Dashboard"""

import streamlit as st
import pandas as pd

# ✅ Page config (only once, at the top)
st.set_page_config(page_title="L'Oréal CommentSense Dashboard", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("/Users/HP/Downloads/sample_comments.csv")
    return df

df = load_data()

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("💬 L'Oréal CommentSense Dashboard")

st.markdown("""
This dashboard analyzes YouTube comments to measure content effectiveness.  
It shows **sentiment**, **spam detection**, and **categorization** of comments.  
""")

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")
sentiment_filter = st.sidebar.multiselect("Select Sentiment", options=df["sentiment"].unique(), default=df["sentiment"].unique())
category_filter = st.sidebar.multiselect("Select Category", options=df["category"].unique(), default=df["category"].unique())
spam_filter = st.sidebar.multiselect("Select Spam/Not Spam", options=df["spam_flag"].unique(), default=df["spam_flag"].unique())

# Apply filters
filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["category"].isin(category_filter)) &
    (df["spam_flag"].isin(spam_filter))
]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

# Define quality condition
quality_df = filtered_df[
    (filtered_df["spam_flag"] == "Not Spam") &
    (filtered_df["sentiment"].isin(["Positive", "Neutral"])) &
    (filtered_df["category"].isin(["skincare", "fragrance", "makeup"]))
]

quality_score = round((len(quality_df) / len(filtered_df)) * 100, 2) if len(filtered_df) > 0 else 0

col1.metric("Total Comments", len(filtered_df))
col2.metric("Quality Comments", len(quality_df))
col3.metric("Spam Comments", len(filtered_df[filtered_df["spam_flag"]=="Spam"]))
col4.metric("Avg Likes (per comment)", round(filtered_df["likeCount_x"].mean(), 2))
col5.metric("Quality Score (%)", f"{quality_score}%")

# -----------------------------
# Sentiment Distribution
# -----------------------------
st.subheader("😊 Sentiment Distribution")
st.bar_chart(filtered_df["sentiment"].value_counts())

# -----------------------------
# Spam Ratio
# -----------------------------
st.subheader("🚫 Spam vs Not Spam")
st.bar_chart(filtered_df["spam_flag"].value_counts())

# -----------------------------
# Category Breakdown
# -----------------------------
st.subheader("💄 Comment Categories")
st.bar_chart(filtered_df["category"].value_counts())

# -----------------------------
# Data Preview
# -----------------------------
st.subheader("🔍 Sample Comments")
st.dataframe(filtered_df[["commentId", "textOriginal", "cleaned_text", "sentiment", "spam_flag", "category"]].head(20))
