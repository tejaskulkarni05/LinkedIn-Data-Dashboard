"""
AI-powered insights generation using Google GenAI.
Generates structured insights about trending topics and patterns in LinkedIn posts.
"""

import os
from typing import Optional, Dict, Any, List
import pandas as pd
import google.genai as genai
from dotenv import load_dotenv

class InsightsGenerator:
    """Generates AI-powered insights from LinkedIn posts using Google GenAI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI generator with API key."""
        load_dotenv()
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. Please set it in Settings page or add it to your .env file."
            )

        self.client = genai.Client(api_key=api_key)

    def _prepare_posts_text(self, top_posts: pd.DataFrame) -> str:
        """Format top posts for AI analysis."""
        posts_text = ""
        
        for idx, row in top_posts.iterrows():
            post_num = idx + 1
            posts_text += f"\n---\nPost {post_num}:\n"
            posts_text += f"Author: {row['author']}\n"
            posts_text += f"Engagement: {int(row['engagement'])}\n"
            posts_text += f"Category: {row['primary_category']}\n"
            posts_text += f"Text:\n{row['post_text']}\n"

        return posts_text

    def generate_insights(
        self,
        top_posts: pd.DataFrame,
        category: str,
    ) -> Dict[str, Any]:
        """
        Generate AI insights from top posts.

        Args:
            top_posts: DataFrame with top posts (should be top 5 per category)
            category: Primary category of posts

        Returns:
            Dictionary with structured insights
        """

        if len(top_posts) < 1:
            return None

        posts_text = self._prepare_posts_text(top_posts)

        prompt = f"""Analyze these top LinkedIn posts from the "{category}" category and provide insights in this exact structure:

{posts_text}

Generate a professional insight summary with this structure:

## What's Trending
(3-4 bullet points about the main themes you see)

## Recurring Angles
(3-4 bullet points about common angles/approaches in these posts)

## Why These Posts Worked
(3-4 bullet points explaining what made them successful - engagement, messaging, timing, etc.)

🧠 **Trend Label:** [One specific trend or shift you identified in 3-5 words]

Keep the insights concise, actionable, and grounded in what you see in the posts. Use markdown formatting.
Make sure insights are valuable for someone trying to understand what's working in the {category} space."""

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            summary_text = response.text if response.text else None

            if not summary_text:
                return None

            return {
                "category": category,
                "post_count": len(top_posts),
                "summary": summary_text,
                "posts_analyzed": top_posts[
                    ["author", "engagement", "primary_category", "post_text", "post_url"]
                ].fillna("").to_dict("records"),
            }

        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return None

    def extract_trend_label(self, summary: str) -> Optional[str]:
        """Extract the trend label from the generated summary."""
        lines = summary.split("\n")
        for line in lines:
            if "🧠 **Trend Label:**" in line or "Trend Label:" in line:
                # Extract text after the label
                label = line.split(":", 1)[-1].strip()
                # Remove markdown formatting
                label = label.replace("**", "").strip()
                return label
        return None
