import streamlit as st
import os
import base64  # For base64-encoding JS to fix MIME/module issues

# Page config for full-width layout (no centering)
st.set_page_config(
    page_title="My HTML App",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Hide Streamlit's default UI elements and fix width/scrolling
# Enhanced CSS for full viewport, reduced errors
st.markdown("""
    <style>
        /* Hide Streamlit menu, footer, and other distractions */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        
        /* Minimize focus/event calls to reduce 403 errors */
        iframe {
            pointer-events: auto !important;
            tabindex: -1;  /* Reduce focus events */
        }
        
        /* Full viewport - no padding/margins, force width */
        .stApp {
            background-color: #000;  /* Match your app's background if needed */
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
        }
        section[data-testid="stAppViewContainer"] {
            padding: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: none !important;
            width: 100vw !important;
            margin: 0 !important;
        }
        
        /* Full-screen embed - targets component and iframe */
        .stMarkdown > div,
        [data-testid="stMarkdownContainer"] > div,
        iframe {
            width: 100vw !important;
            height: 200vh !important;  /* Oversize for full scrolling */
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            position: fixed !important;  /* Full overlay */
            top: 0 !important;
            left: 0 !important;
            z-index: 999 !important;  /* On top */
            overflow: auto !important;  /* Enable scrolling */
        }
    </style>
""", unsafe_allow_html=True)

# Function to inline CSS and JS into HTML (handles modules/MIME fix)
def load_and_inline_html(html_path, css_path, js_path):
    # Read HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Inline CSS: Replace <link href="index.css"> or add <style>
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        # Replace common link patterns (adjust if your href is different)
        html_content = html_content.replace('href="index.css"', 'href=""')  # Disable external load
        html_content = html_content.replace('href=\'index.css\'', 'href=""')  # Single quotes
        # Inject as <style> in <head>
        style_tag = f'<style>{css_content}</style>'
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', style_tag + '</head>')
        else:
            html_content = style_tag + html_content  # Fallback
    
    # Inline JS: Handle modules with base64 data URI to fix MIME errors
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Base64 encode JS for data URI (preserves modules)
        js_b64 = base64.b64encode(js_content.encode('utf-8')).decode('utf-8')
        js_data_uri = f"data:text/javascript;base64,{js_b64}"
        
        # Replace <script src="index.js"> with inline data URI (handles type="module")
        # Common patterns - adjust if your script tag is different
        html_content = html_content.replace('src="index.js"', f'src="{js_data_uri}"')
        html_content = html_content.replace('src=\'index.js\'', f'src="{js_data_uri}"')
        # If no src (inline already), or to ensure module support, add/replace with module script
        if 'type="module"' in html_content or 'index.js' in html_content:
            module_script = f'<script type="module" src="{js_data_uri}"></script>'
            html_content = html_content.replace('</body>', module_script + '</body>')
        else:
            # Fallback for classic JS: Inline directly
            script_tag = f'<script>{js_content}</script>'
            html_content = html_content.replace('</body>', script_tag + '</body>')
    
    # Add full-viewport CSS for scrolling/full size (injected into your app)
    full_screen_css = """
        <style>
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                overflow: auto !important;  /* Scroll when needed */
                box-sizing: border-box;
            }
            /* Target your app's root (adjust '#app' or '.container' to match your HTML) */
            body > * {
                width: 100% !important;
                min-height: 100vh !important;
                overflow: auto !important;
            }
        </style>
    """
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', full_screen_css + '</head>')
    else:
        html_content = full_screen_css + html_content
    
    return html_content

# Paths to your files (root directory)
HTML_PATH = 'index.html'
CSS_PATH = 'index.css'
JS_PATH = 'index.js'

# Check if files exist
if not os.path.exists(HTML_PATH):
    st.error(f"{HTML_PATH} not found! Place it in the same directory as this script.")
    st.stop()

# Load and prepare the HTML with inlined assets (modules fixed)
full_html = load_and_inline_html(HTML_PATH, CSS_PATH, JS_PATH)

# Embed the full HTML app
st.components.v1.html(
    full_html,
    height=None,  # Uses CSS for dynamic height/scrolling
    width=None,   # Full width via CSS
    scrolling=True  # Enable scrolling
)

# Optional: Minimal control (uncomment if needed)
# if st.button("Refresh"):
#     st.rerun()
