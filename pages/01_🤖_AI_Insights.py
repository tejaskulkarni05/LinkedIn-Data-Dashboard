"""
AI Insights Page
Displays AI-generated summaries of top posts per category with evidence.
"""

import streamlit as st
import pandas as pd
from utils.cache_manager import CacheManager
from utils.ai_generator import InsightsGenerator
from components.insights_display import (
    render_insights_card,
    render_comparison_view,
    render_loading_state,
    render_insufficient_data_state,
    render_error_state,
)


def load_data(path: str):
    """Load data from Excel file."""
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
    
    # Ensure post_url column exists and fill missing values
    if "post_url" not in data.columns:
        data["post_url"] = None
    
    return data


# Page config
st.set_page_config(
    page_title="AI Insights",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 AI Insights")
st.markdown("Discover trends and patterns in top LinkedIn posts through AI analysis.")

# Load data
DATA_PATH = "linkedin_posts.xlsx"
data = load_data(DATA_PATH)

# Initialize managers
cache_manager = CacheManager()

# Sidebar configuration
st.sidebar.header("Configuration")

all_authors = sorted(data["author"].unique())
all_categories = sorted(data["primary_category"].dropna().unique())

# Author selection
col1, col2 = st.sidebar.columns([3, 1])
with col1:
    st.write("**Authors**")
with col2:
    select_all_authors = st.checkbox("All", value=True, key="select_all_authors")

selected_authors = st.sidebar.multiselect(
    "Select Authors",
    options=all_authors,
    default=all_authors if select_all_authors else [],
)

# Category selection
col3, col4 = st.sidebar.columns([3, 1])
with col3:
    st.write("**Primary Categories**")
with col4:
    select_all_categories = st.checkbox("All", value=True, key="select_all_categories")

selected_categories = st.sidebar.multiselect(
    "Select Primary Categories",
    options=all_categories,
    default=all_categories if select_all_categories else [],
)

# Filter data
filtered_data = data[
    (data["author"].isin(selected_authors))
    & (data["primary_category"].isin(selected_categories))
]

# Options
st.sidebar.divider()
st.sidebar.subheader("Options")

show_comparison = st.sidebar.checkbox("Show Comparison View", value=False)
show_evidence = st.sidebar.checkbox("Show Evidence Section", value=True)

# Clear cache button
if st.sidebar.button("🗑️ Clear All Cached Insights"):
    cache_manager.clear_cache()
    st.sidebar.success("Cache cleared!")

# Main content
if len(filtered_data) == 0:
    st.warning("No posts found with the selected filters. Please adjust your selections.")
else:
    st.markdown(f"### Analyzing {len(filtered_data)} posts across {len(selected_categories)} categories")
    st.divider()

    # Get unique categories in filtered data
    categories_to_analyze = sorted(filtered_data["primary_category"].unique())

    # Create tabs for each category
    if len(categories_to_analyze) == 1:
        # Single category - no tabs needed
        category = categories_to_analyze[0]
        st.markdown(f"## {category}")

        category_data = filtered_data[filtered_data["primary_category"] == category]

        # Get top 5 posts by engagement
        top_posts = category_data.nlargest(5, "engagement")

        if len(top_posts) < 1:
            render_insufficient_data_state(len(top_posts))
        else:
            # Check cache first
            cached_insights = cache_manager.load_insights(
                category=category,
                authors=selected_authors,
            )

            if cached_insights:
                st.success("📦 Loaded from cache")
                insights = cached_insights["insights"]
            else:
                # Generate new insights
                try:
                    placeholder = st.empty()
                    with placeholder.container():
                        render_loading_state()

                    generator = InsightsGenerator()
                    insights = generator.generate_insights(
                        top_posts=top_posts,
                        category=category,
                    )

                    placeholder.empty()

                    if insights:
                        # Save to cache
                        cache_manager.save_insights(
                            category=category,
                            authors=selected_authors,
                            insights=insights,
                        )
                        st.success("✅ Insights generated successfully!")
                    else:
                        render_error_state("Failed to generate insights")
                        st.stop()

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.stop()

            # Display insights
            if show_comparison:
                render_comparison_view(
                    summary=insights["summary"],
                    posts_analyzed=insights["posts_analyzed"],
                    category=category,
                )
            else:
                render_insights_card(
                    summary=insights["summary"],
                    posts_analyzed=insights["posts_analyzed"],
                    category=category,
                    show_evidence=show_evidence,
                )

    else:
        # Multiple categories - use tabs
        tabs = st.tabs([cat for cat in categories_to_analyze])

        for tab, category in zip(tabs, categories_to_analyze):
            with tab:
                category_data = filtered_data[
                    filtered_data["primary_category"] == category
                ]

                # Get top 5 posts by engagement
                top_posts = category_data.nlargest(5, "engagement")

                if len(top_posts) < 1:
                    render_insufficient_data_state(len(top_posts))
                    continue

                # Check cache first
                cached_insights = cache_manager.load_insights(
                    category=category,
                    authors=selected_authors,
                )

                if cached_insights:
                    st.success("📦 Loaded from cache")
                    insights = cached_insights["insights"]
                else:
                    # Generate new insights
                    insights = None
                    try:
                        placeholder = st.empty()
                        with placeholder.container():
                            render_loading_state()

                        generator = InsightsGenerator()
                        insights = generator.generate_insights(
                            top_posts=top_posts,
                            category=category,
                        )

                        placeholder.empty()

                        if insights:
                            # Save to cache
                            cache_manager.save_insights(
                                category=category,
                                authors=selected_authors,
                                insights=insights,
                            )
                            st.success("✅ Insights generated successfully!")
                        else:
                            render_error_state("Failed to generate insights")
                            continue
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        continue
                
                # Only render if insights were successfully generated/loaded
                if insights:
                    if show_comparison:
                        render_comparison_view(
                            summary=insights["summary"],
                            posts_analyzed=insights["posts_analyzed"],
                            category=category,
                        )
                    else:
                        render_insights_card(
                            summary=insights["summary"],
                            posts_analyzed=insights["posts_analyzed"],
                            category=category,
                            show_evidence=show_evidence,
                        )

    # Footer info
    st.divider()
    st.caption("💡 Insights are cached locally per category and filter combination to reduce token usage.")
