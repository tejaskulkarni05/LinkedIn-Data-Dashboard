# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Multi-Page App                     │
│                        (app.py - entry)                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
    ┌───▼─────┐            ┌──────▼────┐
    │Dashboard│            │AI Insights│
    │(Page 1) │            │ (Page 2)  │
    └────┬────┘            └──────┬────┘
         │                        │
         │                  ┌─────▼──────┐
         │          ┌──────►│Streamlit UI│
         │          │       │Components  │
         │          │       └────────────┘
         │          │
         │    ┌─────▼─────────────┐
         │    │AI Insights Logic  │
         │    │(pages/01_AI...)   │
         │    └─────┬─────────────┘
         │          │
         │     ┌────┴──────────┬──────────────┐
         │     │               │              │
    ┌────▼──┐ ┌▼───────────┐ ┌▼─────────┐  ┌▼────────────┐
    │ Data  │ │Cache Mgmt  │ │AI Gen    │  │Display      │
    │Loading│ │(JSON cache)│ │(GenAI)   │  │Components   │
    └───────┘ └────────────┘ └──────────┘  └─────────────┘
```

## Component Interaction Flow

```
User Opens AI Insights Page
          │
          ▼
Select Authors & Categories
          │
          ▼
User Selects a Category
          │
          ▼
┌─────────────────────────────────┐
│ Check Cache for Results         │
│ (cache_manager.py)              │
└────┬────────────────────────────┘
     │
     ├─ Cache Hit ──────┐
     │                  │
     │             Display Cached
     │             Insights
     │
     └─ Cache Miss ────┐
                       │
                       ▼
              ┌──────────────────┐
              │Load Top 5 Posts  │
              │(by engagement)   │
              └─────┬────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │Generate AI Insights  │
         │(ai_generator.py)     │
         │ - Google GenAI API   │
         └──────┬───────────────┘
                │
                ▼
      ┌────────────────────┐
      │Save to Cache       │
      │(JSON format)       │
      └────┬───────────────┘
           │
           ▼
  ┌─────────────────────┐
  │Display Results      │
  │(insights_display.py)│
  │ - Summary           │
  │ - Evidence Cards    │
  └─────────────────────┘
```

## Data Flow: Cache System

```
Category: "AI"
Authors: ["John", "Jane"]
Filters: {}
    │
    ▼
hash_md5(category|authors|filters)
    │
    ▼
Generate: "abc123def456.json"
    │
    ▼
.cache/abc123def456.json
    │
    ▼
{
  "category": "AI",
  "authors": ["John", "Jane"],
  "filters": {},
  "generated_at": "2024-01-09T10:30:00",
  "insights": {
    "category": "AI",
    "post_count": 5,
    "summary": "...",
    "posts_analyzed": [...]
  }
}
```

## Module Responsibilities

### `pages/00_📊_Dashboard.py`
- **Purpose**: Main analytics dashboard
- **Responsibilities**:
  - Load and filter LinkedIn data
  - Display overview metrics
  - Show category distributions
  - Keyword analysis
  - Top posts ranking
- **Dependencies**: pandas, matplotlib, scikit-learn

### `pages/01_🤖_AI_Insights.py`
- **Purpose**: AI-powered insights page
- **Responsibilities**:
  - UI for category/author selection
  - Orchestrate insight generation workflow
  - Manage caching logic
  - Render insights to user
- **Dependencies**: cache_manager, ai_generator, insights_display

### `utils/cache_manager.py`
- **Purpose**: Local JSON caching
- **Responsibilities**:
  - Generate cache keys from filters
  - Load cached insights
  - Save new insights to cache
  - Clear cache
  - Report cache info
- **Storage**: `.cache/` directory

### `utils/ai_generator.py`
- **Purpose**: Google GenAI integration
- **Responsibilities**:
  - Format posts for AI analysis
  - Call Google GenAI API
  - Parse AI responses
  - Extract trend labels
- **API**: google-genai (Gemini model)

### `components/insights_display.py`
- **Purpose**: UI rendering components
- **Responsibilities**:
  - Render summary in markdown
  - Render evidence cards
  - Display multiple views (card/table)
  - Show loading/error states
  - Comparison view
- **UI Framework**: Streamlit

## Cache Structure

```
.cache/
├── abc123def456.json    # Cache key: hash of (category|authors|filters)
├── def789ghi012.json
├── jkl345mno678.json
└── ...

File contents:
{
  "category": string,
  "authors": array,
  "filters": object,
  "generated_at": ISO timestamp,
  "insights": {
    "category": string,
    "post_count": number,
    "summary": markdown string,
    "posts_analyzed": [
      {
        "author": string,
        "engagement": number,
        "primary_category": string,
        "post_text": string
      }
    ]
  }
}
```

## Data Sources

```
Input: linkedin_posts.xlsx
       │
       ├─ Sheet "Author1" → DataFrame with columns:
       │  ├── post_text
       │  ├── primary_category
       │  ├── total_reactions
       │  ├── comments
       │  ├── reposts
       │  ├── posted_date
       │  ├── is_personal_post
       │  ├── is_reshare
       │  └── post_url
       │
       └─ Sheet "Author2" → Similar structure
       │
       Merged with "author" column added
       │
       Engagement calculated:
       engagement = reactions + comments + reposts
```

## Configuration & Environment

```
.env (required for API key)
├── GOOGLE_API_KEY=sk-...

App Config (page_config):
├── page_title
├── page_icon
├── layout: "wide"
└── initial_sidebar_state: "expanded"

Cache Config (cache_manager.py):
├── cache_dir: ".cache"
└── cache format: JSON with hash filenames
```

## Error Handling & Fallbacks

```
Try to Load Insights
    │
    ├─ No API Key ──────► Error Message
    │
    ├─ Insufficient Data ──► Warning Message
    │
    ├─ API Error ──────────► Error Message + Retry
    │
    ├─ Parse Error ────────► Fallback to None
    │
    └─ Success ───────────► Display Results
```

## Scalability Considerations

### Current Design Handles:
- ✅ Multiple categories (tabbed view)
- ✅ Multiple authors (filter selection)
- ✅ Caching for repeated queries
- ✅ Batch processing within single page load

### Future Enhancements:
- 📈 Scheduled insight generation (Airflow/scheduler)
- 🔄 Incremental cache updates
- 🗄️ Database backend (vs JSON files)
- 📊 Historical trend tracking
- 🎯 Custom AI prompts per segment

## Key Design Decisions

1. **Modular Structure**
   - Separate concerns: caching, AI, UI
   - Easy to test and modify individual components
   - Reusable across multiple pages

2. **Local JSON Caching**
   - Simple, no external dependencies
   - Fast retrieval (no DB calls)
   - Version control friendly
   - Easy to backup/debug

3. **Streamlit Multi-Page**
   - Clean separation of Dashboard vs AI Insights
   - Shared sidebar filters
   - Built-in routing
   - No custom navigation needed

4. **Google GenAI (Flash Model)**
   - Cost-effective
   - Fast inference
   - High-quality summaries
   - Good for text analysis

5. **Markdown Rendering**
   - Universal format
   - Works in all environments
   - Easy to export
   - Readable in source

## Performance Metrics

```
Time Complexity:
- Load data: O(n) where n = total posts
- Filter data: O(n)
- Get top 5: O(n log 5) = O(n)
- Generate insights: O(1) API call
- Load from cache: O(1)

Space Complexity:
- DataFrame: O(n) for all posts
- Cache files: O(p) per category where p = top posts
- Minimal memory footprint for UI

Typical Timings:
- First insight generation: 10-20 seconds (API dependent)
- Cached insights: <1 second
- Page load: <2 seconds
- Data filtering: <1 second
```
