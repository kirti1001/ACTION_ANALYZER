import streamlit as st
import os
import base64
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    # api_key = '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'
    
    try:
        # if hasattr(st, 'secrets') and 'SKVISION' in st.secrets:
            api_key = st.secrets.get['skvision']
            if api_key:
                return api_key
    except Exception as e:
        st.warning("api key not found")
    

# Get API key
api_key = get_api_key()

# DEBUG: Show API key status
st.sidebar.title("🔧 Debug Info")
if api_key:
    st.sidebar.success("✅ API Key Found!")
    st.sidebar.write(f"Key preview: {api_key[:10]}...")
    st.sidebar.write(f"Key length: {len(api_key)}")
else:
    st.sidebar.error("❌ API Key NOT Found!")
    st.sidebar.write("Troubleshooting:")
    st.sidebar.write("1. Check .streamlit/secrets.toml")
    st.sidebar.write("2. Verify SKVISION name matches")
    st.sidebar.write("3. Redeploy after adding secrets")

# STOP if no API key
if not api_key:
    st.error("""
    ## 🔑 API Key Configuration Required
    
    **For Streamlit Cloud:**
    1. Go to your app settings → Secrets
    2. Add: `SKVISION = "your_actual_key_here"`
    
    **File should be at: `.streamlit/secrets.toml`**
    ```toml
    SKVISION = "your_actual_groq_api_key"
    ```
    
    **Current working directory:** 
    """ + os.getcwd())
    st.stop()

# Page config for full-width layout
st.set_page_config(
    page_title="My HTML App",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default UI elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        
        .stApp {
            background-color: transparent !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            height: auto !important;
            overflow: visible !important;
        }
        section[data-testid="stAppViewContainer"] {
            padding: 0 !important;
            width: 100vw !important;
            height: auto !important;
            margin: 0 !important;
            overflow: visible !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: none !important;
            width: 100% !important;
            margin: 0 !important;
            height: auto !important;
            overflow: visible !important;
        }
        
        iframe {
            height: 100% !important;
            width: 100% !important;
            overflow: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

def load_and_inline_html(html_path, css_path, js_path):
    # Read HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Inline CSS as-is
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
    
    # Inline JS with API key injection
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Multiple replacement strategies for API key
        replacements = [
            ('__API_KEY_PLACEHOLDER__', api_key),
            # ('const API_KEY = ""', f'const apiKey = "{api_key}"'),
            # ("const apiKey = ''", f'const apiKey = "{api_key}"'),
            # ('let apiKey = ""', f'let apiKey = "{api_key}"'),
            # ('var apiKey = ""', f'var apiKey = "{api_key}"'),
            # ('YOUR_API_KEY_HERE', api_key),
            # ('API_KEY_PLACEHOLDER', api_key)
        ]
        
        for old, new in replacements:
            js_content = js_content.replace(old, new)
        
        # Also add as global variable
        api_key_injection = f"""
        // Injected API Key
        window.API_KEY = "{api_key}";
        console.log("API Key injected: {api_key[:8]}...");
        """
        js_content = api_key_injection + js_content
        
        js_b64 = base64.b64encode(js_content.encode('utf-8')).decode('utf-8')
        js_data_uri = f"data:text/javascript;base64,{js_b64}"
        html_content = html_content.replace('src="index.js"', f'src="{js_data_uri}"')
        html_content = html_content.replace('src=\'index.js\'', f'src="{js_data_uri}"')
        
        if 'type="module"' in html_content or 'index.js' in html_content:
            module_script = f'<script type="module" src="{js_data_uri}"></script>'
            html_content = html_content.replace('</body>', module_script + '</body>')
        else:
            script_tag = f'<script>{js_content}</script>'
            html_content = html_content.replace('</body>', script_tag + '</body>')
    
    # Add API key verification script
    verification_script = f"""
    <script>
        console.log("API Key available:", "{api_key[:8]}..." );
        // Make API key globally available
        window.INJECTED_API_KEY = "{api_key}";
    </script>
    """
    html_content = html_content.replace('</body>', verification_script + '</body>')
    
    # Minimal injected CSS
    injected_css = """
        <style>
            html, body {
                visibility: visible !important;
                display: block !important;
                height: auto !important;
                overflow: visible !important;
                background: inherit !important;
            }
            * { visibility: visible !important; }
        </style>
    """
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', injected_css + '</head>')
    else:
        html_content = injected_css + html_content
    
    return html_content

# Paths to your files
HTML_PATH = 'index.html'
CSS_PATH = 'index.css'
JS_PATH = 'index.js'

# Check files
if not os.path.exists(HTML_PATH):
    st.error(f"{HTML_PATH} not found!")
    st.sidebar.write("Current directory files:", os.listdir('.'))
    st.stop()

# Load HTML
full_html = load_and_inline_html(HTML_PATH, CSS_PATH, JS_PATH)

# Enhanced debug info
st.sidebar.write("---")
st.sidebar.write("📊 HTML Stats:")
st.sidebar.write(f"HTML Length: {len(full_html)} characters")
st.sidebar.write(f"API Key in HTML: {'✅ Yes' if api_key in full_html else '❌ No'}")
if api_key in full_html:
    st.sidebar.write(f"Key found at position: {full_html.find(api_key)}")

# Show files in current directory
st.sidebar.write("---")
st.sidebar.write("📁 Files in directory:")
try:
    files = os.listdir('.')
    for file in files:
        st.sidebar.write(f" - {file}")
except Exception as e:
    st.sidebar.write(f"Error listing files: {e}")

# Embed via iframe
st.components.v1.html(
    full_html,
    height=3000,
    width=None,
    scrolling=True,
)
