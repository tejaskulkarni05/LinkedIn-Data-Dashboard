"""
Cache manager for storing and retrieving AI-generated insights.
Uses JSON format for local caching to reduce token usage.
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class CacheManager:
    """Manages caching of AI insights locally in JSON format."""

    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(
        self, 
        category: str, 
        authors: list, 
        additional_filters: Dict[str, Any] = None
    ) -> str:
        """Generate a unique cache key based on category and filters."""
        filter_str = f"{category}|{'|'.join(sorted(authors))}"
        
        if additional_filters:
            filter_str += f"|{json.dumps(additional_filters, sort_keys=True)}"
        
        # Create a hash of the filter string for a shorter filename
        hash_key = hashlib.md5(filter_str.encode()).hexdigest()
        return hash_key

    def get_cache_file(self, cache_key: str) -> Path:
        """Get the full path to cache file."""
        return self.cache_dir / f"{cache_key}.json"

    def load_insights(
        self,
        category: str,
        authors: list,
        additional_filters: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """Load cached insights if available."""
        cache_key = self._get_cache_key(category, authors, additional_filters)
        cache_file = self.get_cache_file(cache_key)

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data
            except (json.JSONDecodeError, IOError):
                return None
        return None

    def save_insights(
        self,
        category: str,
        authors: list,
        insights: Dict[str, Any],
        additional_filters: Dict[str, Any] = None
    ) -> bool:
        """Save generated insights to cache."""
        cache_key = self._get_cache_key(category, authors, additional_filters)
        cache_file = self.get_cache_file(cache_key)

        try:
            cache_data = {
                "category": category,
                "authors": authors,
                "filters": additional_filters or {},
                "generated_at": datetime.now().isoformat(),
                "insights": insights,
            }

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def clear_cache(self) -> None:
        """Clear all cached insights."""
        for file in self.cache_dir.glob("*.json"):
            file.unlink()

    def get_cache_info(self) -> Dict[str, Any]:
        """Get information about cached insights."""
        cache_files = list(self.cache_dir.glob("*.json"))
        
        info = {
            "total_cached": len(cache_files),
            "cache_dir": str(self.cache_dir),
            "files": []
        }

        for file in cache_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    info["files"].append({
                        "filename": file.name,
                        "category": data.get("category"),
                        "authors": data.get("authors"),
                        "generated_at": data.get("generated_at"),
                    })
            except (json.JSONDecodeError, IOError):
                continue

        return info
