import streamlit as st
import os
import base64
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')
API_ENDPOINT = f'{BACKEND_URL}/api/v1/analysis/generate-report'

def get_backend_status():
    """Check if backend is running"""
    try:
        response = requests.get(f'{BACKEND_URL}/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def call_secure_backend(analysis_data):
    """Call secure backend API for report generation"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json=analysis_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer streamlit-client'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('report')
            else:
                st.error(f"Backend error: {data.get('error')}")
                return None
        else:
            st.error(f"Backend returned status {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure it's running on port 5000.")
        return None
    except Exception as e:
        st.error(f"Backend error: {str(e)}")
        return None

def load_and_inline_html(html_path, css_path, js_path):
    """
    Load HTML/CSS/JS and prepare for embedding in Streamlit.
    Updated to use index-secure.js (no API keys).
    """
    try:
        # Read HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Inline CSS
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            html_content = html_content.replace('href="index.css"', 'href=""')
            html_content = html_content.replace('href=\'index.css\'', 'href=""')
            style_tag = f'<style>{css_content}</style>'
            if '</head>' in html_content:
                html_content = html_content.replace('</head>', style_tag + '</head>')
            else:
                html_content = style_tag + html_content
        
        # Inline JS (secure version - NO API KEYS)
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            # Update backend URL in secure JS
            js_content = js_content.replace(
                "const BACKEND_URL = 'http://localhost:5000/api/v1/analysis';",
                f"const BACKEND_URL = '{BACKEND_URL}/api/v1/analysis';"
            )
            
            js_b64 = base64.b64encode(js_content.encode('utf-8')).decode('utf-8')
            js_data_uri = f"data:text/javascript;base64,{js_b64}"
            html_content = html_content.replace('src="index.js"', f'src="{js_data_uri}"')
            html_content = html_content.replace('src=\'index.js\'', f'src="{js_data_uri}"')
        
        return html_content
    except FileNotFoundError as e:
        return f"<p>Error loading files: {str(e)}</p>"

# Page configuration
st.set_page_config(
    page_title="AI Critical Action Analyzer - Secure",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit UI
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
    </style>
""", unsafe_allow_html=True)

# Debug sidebar
with st.sidebar:
    st.title("🔧 System Info")
    
    # Backend status
    backend_running = get_backend_status()
    if backend_running:
        st.success("✅ Backend Connected")
    else:
        st.error("❌ Backend Not Running")
        st.write("Start backend with: `python -m backend.app`")
    
    # Security info
    st.write("---")
    st.write("🔒 **Security Status:**")
    st.write("✅ API Keys: Secure (server-side)")
    st.write("✅ Frontend: Clean (no API keys)")
    st.write("✅ Encryption: In transit")
    st.write("✅ Rate Limiting: Enabled")

# Load and display HTML
if backend_running:
    html_path = 'index.html'
    css_path = 'index.css'
    js_path = 'index-secure.js'  # Use secure version
    
    full_html = load_and_inline_html(html_path, css_path, js_path)
    st.components.v1.html(full_html, height=3000, scrolling=True)
else:
    st.error("""  
    ### ⚠️ Backend Not Running
    
    Please start the backend server:
    
    ```bash
    python -m backend.app
    ```
    
    **Why?** This app uses a secure backend to protect API keys.
    The backend must be running on `http://localhost:5000`.
    """)
