"""
Configuration utilities for API keys and settings.
Handles API key retrieval from session state or environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load .env file once
load_dotenv()


def get_gemini_api_key() -> Optional[str]:
    """
    Get Gemini API key with fallback priority:
    1. Session state (user input from settings)
    2. Environment variable (.env file)
    
    Returns:
        API key string if found, None otherwise
    """
    try:
        import streamlit as st
        
        # First check session state (user input from settings)
        if hasattr(st, 'session_state') and 'gemini_api_key' in st.session_state:
            api_key = st.session_state.gemini_api_key
            if api_key and api_key.strip():
                return api_key.strip()
    except ImportError:
        # Not in Streamlit context, skip session state check
        pass
    
    # Fallback to environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key.strip():
        return api_key.strip()
    
    return None

