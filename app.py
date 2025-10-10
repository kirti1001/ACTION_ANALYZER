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

# Hide Streamlit's default UI elements - simplified for visibility
st.markdown("""
    <style>
        /* Hide distractions but keep content visible */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp header {display: none;}
        .stAlert {display: none;}
        
        /* Basic full viewport - no clipping, transparent bg for your dark gradient */
        .stApp {
            background-color: transparent !important;  /* No extra black */
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            height: auto !important;
            overflow: visible !important;  /* Allow content to show */
        }
        section[data-testid="stAppViewContainer"] {
            padding: 0 !important;
            width: 100vw !important;
            height: 10 !important;  /* Expand as needed */
            margin: 0 !important;
            overflow: visible !important;
        }
        .block-container {
            padding: 0 !important;
            max-width: none !important;
            width: 100% !important;
            margin: 0 !important;
            height: 10 !important;  /* No fixed height - let content dictate */
            overflow: visible !important;
        }
        
        /* Iframe - large height for full content visibility, no hiding */
        

    </style>
""", unsafe_allow_html=True)

# Function to inline CSS and JS (unchanged, but added debug)
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
    
    # Inline JS
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
    
    # Minimal injected CSS - only visibility fixes, no overrides that hide content
    injected_css = """
        <style>
            /* Ensure content is visible - no hiding or clipping */
            html, body {
                visibility: visible !important;
                display: block !important;
                height: auto !important;
                overflow: visible !important;  /* Show all sections */
                background: inherit !important;  /* Your dark gradient */
            }
            
            /* Basic anti-hide for sections */
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
    st.stop()

# Load HTML
full_html = load_and_inline_html(HTML_PATH, CSS_PATH, JS_PATH)

# DEBUG: Temporarily show if HTML loaded (comment out after testing)
st.sidebar.title("Debug (Remove After)")
st.sidebar.write(f"HTML Length: {len(full_html)} characters")  # Should be >1000
st.sidebar.code(full_html[:500] + "..." if len(full_html) > 500 else full_html, language="html")  # Preview first 500 chars

# Embed via iframe (large height to show content)
st.components.v1.html(
    full_html,
    height=4000,  # Large to fit full page (scroll to see bottom)
    width=None,
   
)

