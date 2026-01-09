"""
LinkedIn Data Dashboard - Main Entry Point
Multi-page Streamlit application for analyzing LinkedIn thought leader content.

Pages:
- Dashboard: Overview analytics and metrics
- AI Insights: AI-powered trend analysis and insights
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="LinkedIn Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling
# st.markdown("""
#     <style>
#     [data-testid="stSidebar"] {
#         background-color: #544E4D;
#     }
#     </style>
# """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

# Page descriptions
page_info = {
    "📊 Dashboard": "Overview analytics and metrics",
    "🤖 AI Insights": "AI-powered trend analysis per category",
}

st.sidebar.markdown("""
### Available Pages:
- **📊 Dashboard** - Overview analytics and metrics
- **🤖 AI Insights** - AI-powered trend analysis per category

Use the page selector above to navigate.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
This dashboard provides comprehensive analysis of LinkedIn thought leader content,
including traditional analytics and AI-powered insights using Google GenAI.

**Features:**
- Track post engagement across authors and categories
- Analyze trending topics and keywords
- Get AI-generated insights about what's working
- Cached insights for cost efficiency
""")

# Main page info
st.title("📊 LinkedIn Data Dashboard")
st.markdown("""
Welcome to the LinkedIn Data Dashboard! 

This application helps you understand trends and patterns in thought leader content on LinkedIn.
Navigate using the sidebar or the page selector at the top.

### Getting Started:
1. **📊 Dashboard** - Start here to see overview metrics and analytics
2. **🤖 AI Insights** - Discover AI-powered insights about top posts per category

All analytics are computed from your uploaded LinkedIn data.
""")
