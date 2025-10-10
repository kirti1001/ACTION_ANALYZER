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

# Hide Streamlit's default UI elements and optimize for your app's layout
st.markdown("""
    <style>
        /* Hide Streamlit menu, footer, and other distractions */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        
        /* Minimize focus/event calls */
        iframe {
            pointer-events: auto !important;
            tabindex: -1;
        }
        
        /* Full viewport - no padding/margins, but respect app's natural flow */
        .stApp {
            background-color: transparent;  /* Let your dark gradient show */
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;  /* Contain scrolling to iframe */
        }
        section[data-testid="stAppViewContainer"] {
            padding: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            margin: 0 !important;
            overflow: hidden !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: none !important;
            width: 100% !important;
            margin: 0 !important;
            height: 100vh !important;  /* Match viewport for natural scroll */
            overflow: hidden !important;
        }
        
        /* Embed container - full size, no stretching, fix blur */
        .stMarkdown > div,
        [data-testid="stMarkdownContainer"] > div,
        iframe {
            width: 100% !important;  /* Full width, respects your max-widths */
            height: 100vh !important;  /* Exact viewport, no oversize */
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            position: relative !important;  /* Natural flow */
            overflow-y: auto !important;  /* Vertical scroll for long content */
            overflow-x: hidden !important;  /* Match your CSS */
            /* Anti-blur and no scaling (respects your backdrop-filter) */
            filter: none !important;
            backdrop-filter: none !important;  /* Avoid double-blur with your glass effects */
            transform: none !important;
            zoom: 1 !important;
            scale: 1 !important;
        }
        
        /* Ensure fixed navbar doesn't stretch or overlap iframe edges */
        iframe .navbar {
            position: fixed !important;
            top: 0 !important;
            width: 100% !important;
            z-index: 1000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Function to inline CSS and JS into HTML (handles modules/MIME, no CSS mods)
def load_and_inline_html(html_path, css_path, js_path):
    # Read HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Inline your CSS as-is (no changes - preserves gradients, glass, responsive)
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        # Disable external link and inject full CSS
        html_content = html_content.replace('href="index.css"', 'href=""')
        html_content = html_content.replace('href=\'index.css\'', 'href=""')
        style_tag = f'<style>{css_content}</style>'
        if '</head>' in html_content:
            html_content = html_content.replace('</head>', style_tag + '</head>')
        else:
            html_content = style_tag + html_content
    
    # Inline JS (base64 for modules)
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_content = f.read()
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
    
    # Minimal injected CSS: Fix Streamlit integration without stretching your layout
    # Respects your body padding-top, min-height, and overflow-x: hidden
    injected_css = """
        <style>
            /* Minimal overrides for iframe/Streamlit - no stretching */
            html {
                height: auto !important;  /* Allow natural height */
                overflow-x: hidden !important;  /* Match your CSS */
            }
            body {
                height: auto !important;  /* No forced vh - prevents top/bottom black space */
                min-height: 100vh !important;  /* Your existing min-height */
                overflow-y: auto !important;  /* Scroll vertically if content long (e.g., modals, footers) */
                overflow-x: hidden !important;  /* Your setting */
                margin: 0 !important;
                padding: 0 !important;  /* But your padding-top:80px stays for navbar */
                /* Anti-blur/scaling - doesn't affect your glass blur or animations */
                filter: none !important;
                transform: none !important;
                zoom: 1 !important;
            }
            /* No forced height on sections - let your grids/flex flow naturally */
            .hero, .main-container, .areas-section, .footer, .analysis-content, .stats-grid, .skeleton-stats {
                height: auto !important;  /* Prevent stretching */
                min-height: auto !important;
                overflow: visible !important;  /* Allow content to show */
            }
            /* Navbar fixed positioning respected */
            .navbar {
                position: fixed !important;
                top: 0 !important;
                width: 100% !important;
            }
            /* Modal and overlays scroll properly */
            .modal, .modal-body {
                overflow-y: auto !important;
                height: auto !important;
                max-height: 90vh !important;
            }
            /* Responsive media queries untouched - full width on mobile */
            @media (max-width: 1000px) {
                body { padding-top: 70px !important; }  /* Your mobile navbar adjustment */
                .hero, .areas-grid, .stats-grid, .footer-content { width: 100% !important; }
            }
        </style>
    """
    if '</head>' in html_content:
        html_content = html_content.replace('</head>', injected_css + '</head>')
    else:
        html_content = injected_css + html_content
    
    return html_content

# Paths to your files (root directory)
HTML_PATH = 'index.html'
CSS_PATH = 'index.css'
JS_PATH = 'index.js'

# Check if files exist
if not os.path.exists(HTML_PATH):
    st.error(f"{HTML_PATH} not found! Place it in the same directory as this script.")
    st.stop()

# Load and prepare the HTML with inlined assets
full_html = load_and_inline_html(HTML_PATH, CSS_PATH, JS_PATH)

# Embed the full HTML app (optimized for your layout)
st.components.v1.html(
    full_html,
    height=None,  # Dynamic via CSS (100vh container)
    width=None,   # Full width
    scrolling=True  # Vertical scroll enabled
)

# Optional: Refresh button (uncomment if needed; hidden by CSS)
# if st.button("Refresh"):
#     st.rerun()
