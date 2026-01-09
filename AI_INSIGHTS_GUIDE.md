# LinkedIn Data Dashboard - AI Insights Feature

## Overview

The LinkedIn Data Dashboard now includes an advanced **AI Insights** feature that leverages Google GenAI to analyze top posts and generate actionable insights about market trends.

## Features

### 📊 Dashboard Page
- Overview metrics (total posts, engagement, authors)
- Posts distribution by category
- Average engagement by category
- Author profiles and performance
- Top keywords analysis
- Top performing posts

### 🤖 AI Insights Page
- **AI-Powered Summaries**: Automatically analyze top 5 posts per category
- **Structured Insights**: 
  - What's Trending: Key themes in the data
  - Recurring Angles: Common patterns and approaches
  - Why These Posts Worked: Success factors analysis
  - Trend Label: Concise description of the shift
- **Evidence Section**: View original posts that informed the insights
- **Multiple Views**: Card-based or table-based evidence display
- **Local Caching**: JSON-based caching per category to minimize API costs
- **Comparison Mode**: Side-by-side view of summary vs original posts

## Project Structure

```
d:\LinkedinDataDashboard/
├── app.py                          # Main entry point (multi-page navigation)
├── pyproject.toml                  # Project dependencies
├── README.md                        # This file
├── linkedin_posts.xlsx             # Your LinkedIn data
│
├── pages/                          # Streamlit multi-page apps
│   ├── 00_📊_Dashboard.py         # Main analytics dashboard
│   └── 01_🤖_AI_Insights.py       # AI insights generation
│
├── utils/                          # Core functionality
│   ├── __init__.py
│   ├── cache_manager.py           # Local JSON caching system
│   └── ai_generator.py            # Google GenAI integration
│
├── components/                     # UI components
│   ├── __init__.py
│   └── insights_display.py        # Rendering insights and evidence
│
└── .cache/                         # Auto-created folder for cached insights
    └── [hash-based cache files]
```

## How It Works

### 1. Data Selection
Select authors and categories from the sidebar filters in the AI Insights page.

### 2. Top Posts Extraction
The system automatically identifies the top 5 most engaged posts per category.

### 3. AI Analysis
Google GenAI analyzes the posts and generates:
- Trending topics
- Recurring patterns
- Success factors
- Trend labels

### 4. Caching
Results are cached locally in JSON format, keyed by:
- Category
- Selected authors
- Additional filters

Subsequent requests for the same category/author combo load instantly from cache.

### 5. Evidence Display
Original posts are displayed alongside the summary, allowing you to:
- See the analysis context
- Verify the AI's conclusions
- Compare insights with original content

## Usage

### Running the Dashboard

```bash
streamlit run app.py
```

The app will open with navigation to both Dashboard and AI Insights pages.

### Generating AI Insights

1. Navigate to the **AI Insights** page using the sidebar
2. Select your desired authors and categories
3. Click the category tabs to generate insights
4. View the AI summary and evidence sections
5. Use the "Show Comparison View" option to see side-by-side analysis

### Managing Cache

- **View Cache Info**: Check sidebar for cache statistics
- **Clear Cache**: Click "Clear All Cached Insights" in the sidebar to regenerate insights
- **Automatic Caching**: New insights are automatically saved to `.cache/` folder

## Configuration

### Required
- **GOOGLE_API_KEY**: Set in `.env` file or environment variables
  ```
  GOOGLE_API_KEY=your_api_key_here
  ```

### Optional
- Adjust caching directory in `utils/cache_manager.py`
- Modify AI prompt in `utils/ai_generator.py`
- Customize UI components in `components/insights_display.py`

## Data Requirements

The Excel file should have:
- **Columns**: post_text, primary_category, total_reactions, comments, reposts, posted_date, is_personal_post, is_reshare, post_url
- **Sheets**: One sheet per author (sheet name becomes author name)
- **Minimum Posts**: At least 1 post per category (5+ recommended for best insights)

## Cost Optimization

The caching system significantly reduces API costs:
- First insight generation per category: ~1 API call
- Subsequent loads of same category: 0 API calls (cached)
- Cost savings: Up to 90% reduction if filtering by same authors/categories repeatedly

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Ensure your Google API key is set in `.env` file
- Check that python-dotenv is properly loading environment variables

### "Not enough data"
- You need at least 1 post in the selected category
- Try broadening your author/category selection

### Slow insight generation
- First time generation takes ~10-20 seconds depending on post volume
- Subsequent views are instant (cached)
- Clear cache only if you want to regenerate insights

### API Rate Limits
- Space out insight generations if hitting rate limits
- Use category/author filtering to reduce posts analyzed at once

## Future Enhancements

Potential improvements:
- Export insights to PDF
- Scheduled insight generation
- Historical trend tracking
- Custom AI prompts per industry
- Sentiment analysis integration
- Competitive analysis across thought leaders
- Automated recommendations

## Dependencies

Key packages:
- `streamlit>=1.52.2` - Web framework
- `google-genai>=1.57.0` - AI insights generation
- `pandas>=2.3.3` - Data manipulation
- `openpyxl>=3.1.5` - Excel file handling
- `scikit-learn>=1.8.0` - TF-IDF analysis

See `pyproject.toml` for complete list.

## License & Attribution

This dashboard integrates Google GenAI for intelligent content analysis. Ensure you have proper API access and review Google's terms of service.
