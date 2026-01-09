"""
Settings Page
Allows users to configure their Gemini API key and other settings.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Page config
st.set_page_config(
    page_title="Settings",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚙️ Settings")
st.markdown("Configure your API keys and application settings.")

# Load .env file to check for existing key
load_dotenv()
env_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize session state for API key if not exists
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Settings form
with st.form("api_key_settings"):
    st.subheader("🔑 Gemini API Key")
    
    st.markdown("""
    Enter your Google Gemini API key to enable AI insights generation.
    
    **How to get your API key:**
    1. Visit [Google AI Studio](https://ai.google.dev/)
    2. Sign in with your Google account
    3. Create or select an API key
    4. Copy and paste it below
    """)
    
    # Show current status
    if st.session_state.gemini_api_key:
        st.info("✅ API key is set in settings")
    elif env_api_key:
        st.info("ℹ️ Using API key from .env file (fallback)")
    else:
        st.warning("⚠️ No API key found. Please set one below or add it to your .env file.")
    
    # API key input
    api_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        help="Your API key will be stored in session state for this session only.",
        placeholder="Enter your API key here..."
    )
    
    # Form buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        save_button = st.form_submit_button("💾 Save API Key", use_container_width=True)
    
    with col2:
        clear_button = st.form_submit_button("🗑️ Clear API Key", use_container_width=True)
    
    # Handle form submission
    if save_button:
        if api_key_input.strip():
            st.session_state.gemini_api_key = api_key_input.strip()
            st.success("✅ API key saved successfully! It will be used for this session.")
            st.rerun()
        else:
            st.error("❌ Please enter a valid API key.")
    
    if clear_button:
        st.session_state.gemini_api_key = ""
        st.success("🗑️ API key cleared from settings. Will use .env file if available.")
        st.rerun()

# Display current configuration
st.divider()
st.subheader("📋 Current Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**API Key Source:**")
    if st.session_state.gemini_api_key:
        st.success("Settings (User Input)")
    elif env_api_key:
        st.info("Environment File (.env)")
    else:
        st.error("Not Set")

with col2:
    st.markdown("**API Key Status:**")
    if st.session_state.gemini_api_key or env_api_key:
        st.success("✅ Ready to use")
    else:
        st.error("❌ Not configured")

# Additional information
st.divider()
st.markdown("""
### ℹ️ About API Key Storage

- **Settings Input**: The API key you enter here is stored in your browser's session state and will be used for this session only.
- **Environment File**: If no key is set in settings, the app will automatically use the `GOOGLE_API_KEY` from your `.env` file.
- **Priority**: Settings input takes priority over the `.env` file.

### 🔒 Security Note

For production use, it's recommended to use the `.env` file approach as it's more secure and persistent across sessions.
""")

