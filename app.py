import streamlit as st
import os

# Page config for full-width layout (no centering)
st.set_page_config(
    page_title="My HTML App",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar by default
)

# Hide Streamlit's default UI elements for a "full-page" feel
st.markdown("""
    <style>
        /* Hide Streamlit menu, footer, and other distractions */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        /* Make the app full viewport */
        .stApp {
            background-color: #000;  /* Or match your HTML app's background */
        }
        section[data-testid="stAppViewContainer"] {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        /* Full-screen embed */
        iframe {
            width: 100% !important;
            height: 100vh !important;
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Function to inline CSS and JS into HTML
def load_and_inline_html(html_path, css_path, js_path):
    # Read HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Read and inline CSS (replace <link> if present, or add <style>)
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        # Inject CSS into <head> (simple replacement; adjust if your HTML has multiple <head>)
        html_content = html_content.replace('</head>', f'<style>{css_content}</style></head>')
    
    # Read and inline JS (replace <script src> if present, or add <script> before </body>)
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
        # Inject JS before </body> (simple replacement; adjust if needed)
        html_content = html_content.replace('</body>', f'<script>{js_content}</script></body>')
    
    # Add full-viewport CSS to make it truly full-page
    full_screen_css = """
        <style>
            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100vh;
                overflow: hidden;  /* Prevent scrolling if your app doesn't need it */
            }
            #app {  /* Adjust '#app' to match your HTML's root element ID/class */
                width: 100%;
                height: 100vh;
            }
        </style>
    """
    html_content = html_content.replace('</head>', full_screen_css + '</head>')
    
    return html_content

# Paths to your files (adjust if they're in a subfolder like 'static/')
HTML_PATH = 'index.html'
CSS_PATH = 'index.css'
JS_PATH = 'index.js'

# Check if files exist
if not os.path.exists(HTML_PATH):
    st.error(f"index.html not found! Place it in the same directory as this script.")
    st.stop()

# Load and prepare the HTML with inlined assets
full_html = load_and_inline_html(HTML_PATH, CSS_PATH, JS_PATH)

# Embed the full HTML app (no height limit for full-page feel)
st.components.v1.html(
    full_html,
    height=None,  # Let it expand to full height (uses injected CSS)
    width=None,   # Full width
    scrolling=True  # Allow scrolling if your app needs it
)

# Optional: Add a minimal Streamlit control (e.g., refresh button) if needed
# This is hidden by default due to CSS, but you can uncomment if useful
# if st.button("Refresh App"):
#     st.rerun()
