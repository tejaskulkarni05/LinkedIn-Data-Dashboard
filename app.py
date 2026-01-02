import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(page_title="LinkedIn Thought Leader Analysis", layout="wide")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data(path: str):
    xls = pd.ExcelFile(path)
    dfs = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        df["author"] = sheet
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)

    data["engagement"] = (
        data["total_reactions"].fillna(0)
        + data["comments"].fillna(0)
        + data["reposts"].fillna(0)
    )
    return data

DATA_PATH = "linkedin_posts.xlsx"  # place file in same directory
data = load_data(DATA_PATH)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

all_authors = sorted(data["author"].unique())
all_categories = sorted(data["primary_category"].dropna().unique())

col1, col2 = st.sidebar.columns([3, 1])
with col1:
    st.write("**Authors**")
with col2:
    select_all_authors = st.checkbox("All", value=True, key="select_all_authors")

authors = st.sidebar.multiselect(
    "Select Authors",
    options=all_authors,
    default=all_authors if select_all_authors else []
)

col3, col4 = st.sidebar.columns([3, 1])
with col3:
    st.write("**Primary Categories**")
with col4:
    select_all_categories = st.checkbox("All", value=True, key="select_all_categories")

categories = st.sidebar.multiselect(
    "Select Primary Categories",
    options=all_categories,
    default=all_categories if select_all_categories else []
)

filtered = data[
    (data["author"].isin(authors)) &
    (data["primary_category"].isin(categories))
]

# -----------------------------
# Header Metrics
# -----------------------------
st.title("📊 LinkedIn Thought Leader Analysis")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Posts", len(filtered))
col2.metric("Unique Authors", filtered["author"].nunique())
col3.metric("Total Engagement", int(filtered["engagement"].sum()))
col4.metric("Avg Engagement / Post", round(filtered["engagement"].mean(), 2))

st.divider()

# -----------------------------
# Category Distribution
# -----------------------------
st.subheader("Posts Distribution by Primary Category")

cat_counts = filtered["primary_category"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(cat_counts, labels=cat_counts.index, autopct="%1.1f%%")
ax1.set_ylabel("")
st.pyplot(fig1)

# -----------------------------
# Engagement by Category
# -----------------------------
st.subheader("Average Engagement by Category")

eng_by_cat = (
    filtered.groupby("primary_category")["engagement"]
    .mean()
    .sort_values(ascending=False)
)

if not eng_by_cat.empty:
    fig2, ax2 = plt.subplots()
    eng_by_cat.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Average Engagement")
    st.pyplot(fig2)
else:
    st.info("No data available for the selected filters.")

# -----------------------------
# Author Deep Dive
# -----------------------------
st.subheader("Author-wise Deep Profiles")

author_summary = (
    filtered.groupby("author")
    .agg(
        total_posts=("post_text", "count"),
        avg_engagement=("engagement", "mean"),
        total_engagement=("engagement", "sum"),
        personal_pct=("is_personal_post", "mean"),
        reshared_pct=("is_reshare", "mean"),
    )
    .reset_index()
)

author_summary["personal_pct"] = (author_summary["personal_pct"] * 100).round(2)
author_summary["reshared_pct"] = (author_summary["reshared_pct"] * 100).round(2)
author_summary["avg_engagement"] = author_summary["avg_engagement"].round(2)

author_summary = author_summary.sort_values("total_engagement", ascending=False)

st.dataframe(author_summary, width='stretch')

# -----------------------------
# Keyword Analysis
# -----------------------------
st.subheader("Top Keywords (TF-IDF)")

texts = filtered["post_text"].dropna().astype(str)

if len(texts) > 5:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=30)
    tfidf = vectorizer.fit_transform(texts)

    keywords = vectorizer.get_feature_names_out()
    scores = tfidf.sum(axis=0).A1

    kw_df = (
        pd.DataFrame({"keyword": keywords, "importance": scores})
        .sort_values("importance", ascending=False)
    )

    st.dataframe(kw_df, width='stretch')
else:
    st.info("Not enough text data for keyword extraction.")

# -----------------------------
# Top Posts
# -----------------------------
st.subheader("Top Performing Posts")

cols = ["author", "posted_date", "primary_category", "engagement", "post_url"]

st.dataframe(
    filtered.sort_values("engagement", ascending=False)[cols].head(15),
    width='stretch'
)

st.caption("All analytics computed directly from uploaded data. No synthetic values used.")
