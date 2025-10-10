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
# Enhanced CSS to fix width, scrolling, and suppress errors
st.markdown("""
    <style>
        /* Hide Streamlit menu, footer, and other distractions */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        
        /* Suppress focus/event errors in embed (fixes 403) */
        iframe { pointer-events: auto; }  /* Allow interactions */
        
        /* Make the app full viewport - no padding/margins */
        .stApp {
            background-color: #000;  /* Match your app's background if needed */
            margin: 0 !important;
            padding: 0 !important;
        }
        section[data-testid="stAppViewContainer"] {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
        }
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: none !important;
        }
        
        /* Full-screen iframe/embed - targets the component container */
        .stMarkdown > div > iframe,
        [data-testid="stMarkdownContainer"] > iframe,
        iframe {
            width: 100vw !important;
            height: 200vh !important;  /* Oversize for full scrollable viewport */
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            position: fixed !important;  /* Overlay for true full-screen feel */
            top: 0 !important;
            left: 0 !important;
            z-index: 1 !important;
        }
        
        /* Injected styles for your HTML app (applied via static HTML) */
        /* Add this to your index.html <head> if needed, or it will be served as-is */
    </style>
""", unsafe_allow_html=True)

# Paths to static files
STATIC_PATH = 'index.html'

# Check if static file exists
if not os.path.exists(STATIC_PATH):
    st.error(f"{STATIC_PATH} not found! Create a 'static/' folder and place index.html, index.css, index.js there.")
    st.stop()

# Optional: Inject full-viewport CSS directly into the static HTML for scrolling/full size
# (Read and modify index.html to add CSS - preserves modules/JS)
def inject_full_viewport_css(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    full_screen_css = """
        <style>
            html, body {
                margin: 0 !important;
                padding: 0 !important;
                width: 100vw !important;
                height: 100vh !important;  /* Full viewport */
                overflow: auto !important;  /* Enable scrolling when needed */
                box-sizing: border-box;
            }
            /* Adjust to your app's root element (e.g., #app, .container, body > div) */
            body > * {  /* Targets direct children of body */
                width: 100% !important;
                height: 100% !important;
                overflow: auto !important;  /* Scrollable content */
            }
        </style>
    """
    # Inject into <head> (safe even if multiple <head>)
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', full_screen_css + '</head>')
    else:
        html_content = full_screen_css + html_content  # Fallback: add before <body>
    
    return html_content

# Load and inject CSS into the static HTML (for full viewport/scrolling)
full_static_html = inject_full_viewport_css(STATIC_PATH)

# Write the modified HTML temporarily to static/ (for iframe src)
temp_html_path = 'static/index_full.html'
with open(temp_html_path, 'w', encoding='utf-8') as f:
    f.write(full_static_html)

# Embed via iframe (uses static serving - preserves JS modules, CSS links)
# src points to the temp full HTML (served at /static/index_full.html)
st.components.v1.iframe(
    src="./index.html",  # Relative to Streamlit server
    width=None,  # Full width (uses CSS)
    height=2000,  # Large height for scrolling (adjust if needed; CSS handles vh)
    scrolling=True  # Enable scrolling
)

# Clean up temp file (optional, but keeps things tidy)
# os.remove(temp_html_path)  # Uncomment if you want to delete after serving
