# Implementation Details & Customization Guide

## How to Customize the Feature

### 1. Modify AI Prompt (Tailor Insights to Your Needs)

**File**: `utils/ai_generator.py`

Current prompt in `generate_insights()` method:

```python
prompt = f"""Analyze these top LinkedIn posts from the "{category}" category and provide insights in this exact structure:
...
```

**To customize**, edit the prompt template. Examples:

#### Focus on Specific Industries
```python
prompt = f"""Analyze these top AI/ML LinkedIn posts and provide insights specifically for:
- Machine Learning practitioners
- Data Scientists
- AI Engineers

Structure your response with:
...
"""
```

#### Add Sentiment Analysis
```python
prompt = f"""Analyze these posts and provide:
1. Trending topics
2. Sentiment patterns (positive, neutral, critical)
3. Call-to-action types
...
"""
```

#### Competitive Analysis
```python
prompt = f"""Compare these posts from the "{category}" space and identify:
1. What competitors are talking about
2. Unique angles used by top performers
3. Gaps in current conversations
...
"""
```

### 2. Change Cache Directory

**File**: `pages/01_🤖_AI_Insights.py`

Change the cache directory initialization:

```python
# Default: .cache
cache_manager = CacheManager(cache_dir=".cache")

# Custom: store in subdirectory
cache_manager = CacheManager(cache_dir="data/insights_cache")

# Custom: absolute path
cache_manager = CacheManager(cache_dir="/var/cache/linkedin_insights")
```

### 3. Adjust Top Posts Count

**File**: `pages/01_🤖_AI_Insights.py`

Currently analyzes top 5 posts. To change:

```python
# Current
top_posts = category_data.nlargest(5, "engagement")

# Change to top 10
top_posts = category_data.nlargest(10, "engagement")

# Change to top 3
top_posts = category_data.nlargest(3, "engagement")
```

Also update in prompt if you want AI to reference correct count:

```python
prompt = f"""Analyze these top {len(top_posts)} LinkedIn posts...
"""
```

### 4. Customize UI Layout

**File**: `components/insights_display.py`

#### Change Card Display
```python
# Current: border=True
with st.container(border=True):
    ...

# Alternative: colored container
with st.container():
    st.markdown("---")
    ...
```

#### Adjust Column Ratios
```python
# Current: 3:1 ratio
col1, col2 = st.columns([3, 1])

# Change to: 2:1 ratio
col1, col2 = st.columns([2, 1])

# Change to: 1:1 ratio
col1, col2 = st.columns([1, 1])
```

#### Reorder Metrics
```python
# In render_insights_card(), move metrics:
with col2:
    st.markdown("### Quick Stats")
    # Reorder these:
    st.metric("Posts Analyzed", len(posts_analyzed))
    st.metric("Total Engagement", int(total_engagement))
    st.metric("Avg Engagement", f"{avg_engagement:.0f}")
```

### 5. Filter Settings

**File**: `pages/01_🤖_AI_Insights.py`

#### Add Engagement Threshold
```python
# After filtering, add:
MIN_ENGAGEMENT = 10
top_posts = top_posts[top_posts["engagement"] >= MIN_ENGAGEMENT]

if len(top_posts) < 5:
    st.warning(f"Only {len(top_posts)} posts above engagement threshold")
```

#### Add Date Range Filter
```python
# Add to sidebar
date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        filtered_data["posted_date"].min(),
        filtered_data["posted_date"].max()
    )
)

filtered_data = filtered_data[
    (filtered_data["posted_date"] >= date_range[0]) &
    (filtered_data["posted_date"] <= date_range[1])
]
```

#### Add Engagement Type Filter
```python
engagement_type = st.sidebar.radio(
    "Filter by Engagement Type",
    options=["All", "High Reactions", "High Comments", "High Reposts"]
)

if engagement_type == "High Reactions":
    filtered_data = filtered_data[
        filtered_data["total_reactions"] > filtered_data["total_reactions"].median()
    ]
```

### 6. Cache Strategy Customization

**File**: `utils/cache_manager.py`

#### Add TTL (Time-To-Live)
```python
import time
from datetime import datetime, timedelta

def load_insights(self, category, authors, ttl_hours=24):
    """Load cached insights if available and not expired."""
    cache_data = self._load_cache_file(...)
    
    if cache_data:
        generated_time = datetime.fromisoformat(cache_data["generated_at"])
        age_hours = (datetime.now() - generated_time).total_seconds() / 3600
        
        if age_hours < ttl_hours:
            return cache_data["insights"]
    
    return None
```

#### Add Versioning
```python
def save_insights(self, category, authors, insights):
    cache_data = {
        "version": "1.0",  # Add version
        "category": category,
        "authors": authors,
        "generated_at": datetime.now().isoformat(),
        "insights": insights,
    }
    # ... save as before
```

### 7. Add Additional Insight Sections

**File**: `utils/ai_generator.py`

Modify the prompt to include additional analysis:

```python
prompt = f"""Generate insights with these sections:

## What's Trending
[3-4 bullets]

## Recurring Angles  
[3-4 bullets]

## Why These Posts Worked
[3-4 bullets]

## Content Type Breakdown
[Analyze post formats used]

## Audience Response Patterns
[What types of engagement each post gets]

## Recommended Content Angles
[New angles not yet explored]

🧠 **Trend Label:** [One phrase]
"""
```

### 8. Error Handling Customization

**File**: `pages/01_🤖_AI_Insights.py`

#### Retry Logic
```python
from typing import Optional

def generate_with_retry(generator, posts, category, max_retries=3):
    for attempt in range(max_retries):
        try:
            return generator.generate_insights(posts, category)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            st.warning(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff
```

#### Fallback Behavior
```python
if insights is None:
    st.warning("""
    AI insight generation failed. Showing evidence only.
    Please check your API key and try again.
    """)
    render_evidence_section(top_posts.to_dict("records"))
```

### 9. Add Export Functionality

**File**: `components/insights_display.py`

```python
import json
from datetime import datetime

def add_export_buttons(insights, category):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export as JSON"):
            json_str = json.dumps(insights, indent=2)
            st.download_button(
                "Download JSON",
                json_str,
                file_name=f"insights_{category}_{datetime.now().strftime('%Y%m%d')}.json"
            )
    
    with col2:
        if st.button("📄 Export as Markdown"):
            md_content = f"# {category} Insights\n\n{insights['summary']}"
            st.download_button(
                "Download Markdown",
                md_content,
                file_name=f"insights_{category}_{datetime.now().strftime('%Y%m%d')}.md"
            )
    
    with col3:
        if st.button("📋 Copy as Text"):
            st.code(insights['summary'], language="markdown")
```

### 10. Performance Optimization

#### Cache Pre-warming
```python
# In AI Insights page, at startup:
@st.cache_resource
def preload_cache():
    cache_manager = CacheManager()
    categories = filtered_data["primary_category"].unique()
    
    for category in categories:
        if cache_manager.load_insights(category, selected_authors) is None:
            st.info(f"Pre-generating cache for {category}...")
            # Generate insights in background
```

#### Pagination for Large Results
```python
def render_evidence_section_paginated(posts_analyzed, per_page=5):
    total_pages = (len(posts_analyzed) + per_page - 1) // per_page
    page = st.select_slider("Page", 1, total_pages)
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    for post in posts_analyzed[start_idx:end_idx]:
        # Render post
```

## Configuration Examples

### Minimal Configuration (Default)
```python
# uses defaults:
# - cache_dir = ".cache"
# - top_posts = 5
# - no TTL (cache forever)

cache_manager = CacheManager()
generator = InsightsGenerator()
```

### Production Configuration
```python
# Optimized for production
cache_manager = CacheManager(cache_dir="/var/lib/insights_cache")

# With error handling
try:
    generator = InsightsGenerator()
except ValueError:
    st.error("API key not configured. See docs.")
    st.stop()

# With rate limiting
import asyncio
from functools import lru_cache

@lru_cache(maxsize=10)
def get_generator():
    return InsightsGenerator()
```

### Development Configuration
```python
# For testing/debugging
cache_manager = CacheManager(cache_dir=".cache_test")

# Clear cache between runs
cache_manager.clear_cache()

# Verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Testing Customizations

### Unit Test Example
```python
# test_cache_manager.py
import pytest
from utils.cache_manager import CacheManager

def test_cache_key_generation():
    cm = CacheManager()
    key1 = cm._get_cache_key("AI", ["john", "jane"])
    key2 = cm._get_cache_key("AI", ["jane", "john"])
    assert key1 == key2  # Order shouldn't matter
```

### Integration Test Example
```python
# test_ai_insights.py
def test_insights_generation():
    generator = InsightsGenerator()
    top_posts = get_sample_posts()
    
    insights = generator.generate_insights(top_posts, "AI")
    
    assert insights is not None
    assert "summary" in insights
    assert len(insights["posts_analyzed"]) == len(top_posts)
```

## Monitoring & Logging

Add logging to track AI usage:

```python
import logging

logger = logging.getLogger(__name__)

class InsightsGenerator:
    def generate_insights(self, top_posts, category):
        logger.info(f"Generating insights for {category} with {len(top_posts)} posts")
        
        try:
            result = self.model.generate_content(prompt)
            logger.info(f"Successfully generated insights for {category}")
            return result
        except Exception as e:
            logger.error(f"Failed to generate insights: {str(e)}")
            raise
```

## Common Customization Patterns

| Need | File | Change |
|------|------|--------|
| Change prompt | `ai_generator.py` | Edit `prompt` variable in `generate_insights()` |
| Change cache location | `01_🤖_AI_Insights.py` | Pass `cache_dir` to `CacheManager()` |
| Analyze more posts | `01_🤖_AI_Insights.py` | Change `.nlargest(5, ...)` to `.nlargest(10, ...)` |
| Different AI model | `ai_generator.py` | Change `genai.GenerativeModel("gemini-2.0-flash-exp")` |
| Export results | `insights_display.py` | Add export buttons component |
| Filter by date | `01_🤖_AI_Insights.py` | Add date range selector in sidebar |
| Rate limiting | `ai_generator.py` | Add `time.sleep()` between requests |
| Sentiment analysis | `ai_generator.py` | Modify prompt to request sentiment |
| Database instead of JSON | `cache_manager.py` | Replace file ops with DB queries |

## Need Help?

- **Documentation**: See `AI_INSIGHTS_GUIDE.md`
- **Quick Start**: See `QUICKSTART.md`
- **Architecture**: See `ARCHITECTURE.md`
- **Code Examples**: This file has many!
