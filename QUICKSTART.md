# AI Insights Feature - Quick Start Guide

## What's New?

Your LinkedIn Data Dashboard now has a powerful AI Insights feature that automatically analyzes top posts and generates actionable insights using Google GenAI.

## Quick Setup

### 1. Install Dependencies
All dependencies are already in `pyproject.toml`. If needed, install them:

```bash
uv sync
# or
pip install google-genai python-dotenv
```

### 2. Set Up Google API Key

Add your Google API key to the `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://ai.google.dev/

### 3. Run the App

```bash
streamlit run app.py
```

This opens a multi-page app with:
- **📊 Dashboard** - Original analytics (unchanged)
- **🤖 AI Insights** - NEW AI-powered insights page

## Using AI Insights

### Step-by-Step

1. **Navigate to AI Insights Page**
   - Click "AI Insights" in the sidebar or page selector

2. **Configure Filters** (optional)
   - Select specific authors
   - Select specific categories
   - Leave as "All" to analyze everything

3. **View Insights**
   - For each category, the app shows:
     - **What's Trending** - Main themes
     - **Recurring Angles** - Common patterns
     - **Why These Posts Worked** - Success factors
     - **Trend Label** - Concise trend description

4. **Review Evidence**
   - Below each summary, see the top 5 posts that informed the analysis
   - Switch between "Card View" and "Table View"
   - Click "Read full post" to see complete text

5. **Optional: Comparison View**
   - Enable in sidebar to see summary and original posts side-by-side
   - Useful for verifying AI analysis

### Features

✅ **Automatic Caching**
- First analysis per category generates insights
- Subsequent views load instantly from cache
- Reduces API costs by ~90%

✅ **Multiple Category Support**
- Single category: Full-page view
- Multiple categories: Tab-based navigation

✅ **Smart Evidence Display**
- Card-based view: Nice visual presentation
- Table view: Compact overview
- Full post access: Click to expand

✅ **Cache Management**
- Sidebar shows cache info
- "Clear All Cached Insights" to regenerate

## What the AI Analyzes

The AI looks at:
1. **Top 5 Most Engaged Posts** per category
2. **Text Content** - What they talk about
3. **Engagement Metrics** - Reactions, comments, reposts
4. **Patterns** - Recurring themes and angles

Then it generates:
- Trending topics in markdown format
- Actionable insights about what works
- A concise trend label summarizing the shift

## Understanding the Output

### What's Trending
Lists 3-4 main topics/themes in the top posts

### Recurring Angles
Shows 3-4 common approaches or perspectives used in successful posts

### Why These Posts Worked
Explains 3-4 success factors (messaging, timing, audience, etc.)

### Trend Label
A single phrase capturing the overall shift (e.g., "From hype to pragmatism")

### Evidence Section
Original posts with:
- Author name
- Engagement count
- Shortened preview
- Link to expand full text

## Tips for Best Results

1. **More Posts = Better Insights**
   - 5+ posts per category recommended
   - Minimum 1 post required

2. **Filter by Context**
   - Analyze specific authors together
   - Focus on relevant categories
   - Remove outlier data if needed

3. **Use Caching Smartly**
   - Run insights once, view many times
   - Clear cache only when data updates
   - Batch similar analyses together

4. **Verify AI Conclusions**
   - Always review the evidence section
   - Check if trends match your expectations
   - Use insights as starting points, not final truths

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GOOGLE_API_KEY not found" | Add key to `.env` file |
| "Not enough data" | Add more posts or broaden filters |
| Slow generation | Normal (10-20s first time, instant after) |
| Want new insights | Click "Clear All Cached Insights" |
| API errors | Check API key validity and rate limits |

## File Structure

```
New files added:
├── pages/00_📊_Dashboard.py      ← Dashboard (moved from app.py)
├── pages/01_🤖_AI_Insights.py    ← AI Insights (NEW)
├── utils/cache_manager.py         ← Caching system (NEW)
├── utils/ai_generator.py          ← Google GenAI integration (NEW)
├── components/insights_display.py ← UI components (NEW)
├── AI_INSIGHTS_GUIDE.md           ← Full documentation (NEW)
└── app.py                         ← Updated entry point

Auto-created:
└── .cache/                        ← Cached insights (auto-created)
```

## Cost Considerations

Using Google GenAI's Flash model (very cost-effective):
- ~0.075 tokens per 1000 characters analyzed
- 5 posts × 300 chars = ~1,500 chars = ~0.11 tokens per analysis
- Cache reduces most requests to 0 API calls

## Next Steps

1. Set your Google API key in `.env`
2. Run `streamlit run app.py`
3. Navigate to AI Insights page
4. Select authors/categories
5. Watch the magic happen! 🚀

Any questions? Check `AI_INSIGHTS_GUIDE.md` for detailed documentation.
