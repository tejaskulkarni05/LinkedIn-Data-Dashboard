"""
UI components for displaying AI-generated insights and evidence.
Handles rendering of summaries and original posts in a user-friendly format.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional


def render_summary_section(summary_text: str) -> None:
    """Render the AI-generated summary in markdown format."""
    st.markdown(summary_text)


def render_evidence_section(posts_analyzed: list) -> None:
    """
    Render original posts as evidence for the insights.

    Args:
        posts_analyzed: List of post dictionaries with author, engagement, and text
    """
    st.subheader("📚 Evidence: Top Posts Behind This Insight")

    # Create tabs for different views
    tab1, tab2 = st.tabs(["Card View", "Table View"])

    with tab1:
        # Card-style display - better UX
        for idx, post in enumerate(posts_analyzed, 1):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(
                        f"""**Post {idx}** • {post['author']} • 📊 {int(post['engagement'])} engagement""",
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.metric("Engagement", int(post["engagement"]))

                # Post text preview - handle NaN/None values
                post_text = post.get("post_text", "")
                
                # Convert to string and handle NaN values
                if post_text is None or (isinstance(post_text, float) and pd.isna(post_text)):
                    post_text = "[Post text not available]"
                else:
                    post_text = str(post_text)
                
                preview_length = 300
                if len(post_text) > preview_length:
                    preview = post_text[:preview_length] + "..."
                else:
                    preview = post_text

                st.write(preview)

                # Show full text and link in expander
                with st.expander("📖 Read full post"):
                    st.write(post_text)
                    
                    # Add link to original post if available
                    post_url = post.get("post_url")
                    if post_url and not (isinstance(post_url, float) and pd.isna(post_url)):
                        st.markdown(f"[🔗 View original post on LinkedIn]({post_url})", unsafe_allow_html=True)

    with tab2:
        # Table view
        def get_post_preview(post):
            post_text = post.get("post_text", "")
            if post_text is None or (isinstance(post_text, float) and pd.isna(post_text)):
                return "[Post text not available]"
            post_text = str(post_text)
            return post_text[:150] + "..." if len(post_text) > 150 else post_text
        
        def get_post_url(post):
            post_url = post.get("post_url")
            if post_url and not (isinstance(post_url, float) and pd.isna(post_url)):
                return f"[🔗 Link]({post_url})"
            return "N/A"
        
        display_df = pd.DataFrame([
            {
                "Author": post["author"],
                "Engagement": int(post["engagement"]),
                "Category": post.get("primary_category", "N/A"),
                "Post Preview": get_post_preview(post),
                "Link": get_post_url(post),
            }
            for post in posts_analyzed
        ])

        st.dataframe(display_df, width='stretch', hide_index=True)


def render_loading_state() -> None:
    """Render loading spinner and message."""
    st.info("⏳ Generating AI insights... This may take a moment.")
    with st.spinner("Analyzing posts and generating insights..."):
        pass


def render_insufficient_data_state(post_count: int) -> None:
    """Render message when there aren't enough posts for analysis."""
    st.warning(
        f"⚠️ Not enough data: Found only {post_count} post(s) in this category. "
        f"Need at least 1 post for insights."
    )


def render_error_state(error_msg: str) -> None:
    """Render error message."""
    st.error(f"❌ Error generating insights: {error_msg}")


def render_insights_card(
    summary: str,
    posts_analyzed: list,
    category: str,
    show_evidence: bool = True,
) -> None:
    """
    Render complete insights card with summary and evidence.

    Args:
        summary: AI-generated summary text
        posts_analyzed: List of analyzed posts
        category: Category name
        show_evidence: Whether to show evidence section
    """
    # Header
    st.markdown(f"## 🎯 AI Insights: {category}")
    st.divider()

    # Summary section
    col1, col2 = st.columns([3, 1], gap="large")

    with col1:
        st.markdown("### Summary")
        render_summary_section(summary)

    with col2:
        st.markdown("### Quick Stats")
        st.metric("Posts Analyzed", len(posts_analyzed))
        total_engagement = sum(post["engagement"] for post in posts_analyzed)
        st.metric("Total Engagement", int(total_engagement))
        avg_engagement = total_engagement / len(posts_analyzed)
        st.metric("Avg Engagement", f"{avg_engagement:.0f}")

    st.divider()

    # Evidence section
    if show_evidence:
        render_evidence_section(posts_analyzed)


def render_comparison_view(
    summary: str,
    posts_analyzed: list,
    category: str,
) -> None:
    """
    Render a side-by-side comparison view of summary vs original posts.

    Args:
        summary: AI-generated summary
        posts_analyzed: Original posts
        category: Category name
    """
    st.markdown(f"## 📊 Insights vs Evidence: {category}")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### 🤖 AI Summary")
        render_summary_section(summary)

    with col2:
        st.markdown("### 📌 Original Posts")
        for idx, post in enumerate(posts_analyzed[:5], 1):
            st.markdown(f"**Post {idx}** • {post['author']}")
            st.caption(f"Engagement: {int(post['engagement'])}")
            
            # Handle post text with NaN/None values
            post_text = post.get("post_text", "")
            if post_text is None or (isinstance(post_text, float) and pd.isna(post_text)):
                post_text = "[Post text not available]"
            else:
                post_text = str(post_text)
            
            st.text(post_text[:200] + "..." if len(post_text) > 200 else post_text)
            
            # Add link to original post if available
            post_url = post.get("post_url")
            if post_url and not (isinstance(post_url, float) and pd.isna(post_url)):
                st.markdown(f"[🔗 View on LinkedIn]({post_url})")
            
            st.divider()
