import streamlit as st
import requests
import base64

# Page configuration
st.set_page_config(
    page_title="AI Critical Action Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Streamlit app
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0ea5e9;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .embed-container {
        border: 2px solid #3b82f6;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        height: 1000px;
    }
    .fallback-btn {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        border: none;
        width: 100%;
        height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load and modify HTML content
@st.cache_data(ttl=3600)
def load_modified_html_content():
    try:
        # Load from local file
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        # Fallback to GitHub
        github_raw_url = "https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/main/index.html"
        response = requests.get(github_raw_url)
        response.raise_for_status()
        html_content = response.text
    
    # Inject CSS directly into the HTML
    css_content = """
    <style>
    /* Add your index.css content here */
    body {
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        max-width: 1200px;
        width: 95%;
        margin: 2rem auto;
    }
    
    /* Add more of your CSS styles here */
    </style>
    """
    
    # Insert CSS into head section
    if '<head>' in html_content:
        html_content = html_content.replace('<head>', '<head>' + css_content)
    else:
        html_content = css_content + html_content
    
    return html_content

# Alternative: Create a complete standalone HTML with all CSS/JS embedded
def create_standalone_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Action Analyzer</title>
        <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.waves.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            #vanta-bg {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                max-width: 1200px;
                width: 95%;
                margin: 2rem auto;
                position: relative;
                z-index: 1;
            }
            
            .header {
                text-align: center;
                margin-bottom: 2rem;
            }
            
            .header h1 {
                color: #2d3748;
                margin-bottom: 0.5rem;
                font-size: 2.5rem;
            }
            
            .header p {
                color: #4a5568;
                font-size: 1.1rem;
            }
            
            /* Add the rest of your CSS styles here */
            
        </style>
    </head>
    <body>
        <div id="vanta-bg"></div>
        <div class="container">
            <div class="header">
                <h1>AI Action Analyzer</h1>
                <p>Real-time pose detection and analysis</p>
            </div>
            <!-- Your existing HTML content here -->
            <div style="text-align: center; padding: 2rem;">
                <h3>Analysis Interface</h3>
                <p>Camera and pose detection features would appear here.</p>
                <p><em>Note: Some features may be limited in embedded mode.</em></p>
            </div>
        </div>
        
        <script>
            // Initialize Vanta.js waves background
            if(typeof VANTA !== 'undefined') {
                VANTA.WAVES({
                    el: "#vanta-bg",
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: 200.00,
                    minWidth: 200.00,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x3b82f6,
                    shininess: 0.00,
                    waveHeight: 20.00,
                    waveSpeed: 0.50,
                    zoom: 0.65
                });
            }
            
            // Your existing JavaScript code here
        </script>
    </body>
    </html>
    """

# Sidebar
with st.sidebar:
    st.title("📋 About the Analyzer")
    st.markdown("""
    ### Key Features
    - **Pose Detection**: Uses MediaPipe for real-time body landmark tracking.
    - **Metrics Analysis**: Posture, balance, symmetry, and motion scoring.
    - **AI Reports**: Generates professional insights via LLM.
    - **Offline Capable**: Works in browser with fallback local reports.
    """)

# Main content
st.markdown('<h1 class="main-header">🤖 AI Based Critical Action Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Unlock insights into your posture, balance, and movement with AI-powered pose analysis</p>', unsafe_allow_html=True)

# Features in columns
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="feature-box">🔍 **Real-Time Pose Tracking**<br>Detect 33 body landmarks with high accuracy using MediaPipe.</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-box">📊 **Smart Metrics & Reports**<br>Get scores for posture, balance, symmetry, and motion.</div>', unsafe_allow_html=True)

st.divider()

# Embed the modified HTML
st.markdown("### 🚀 Launching the Analyzer...")

try:
    # Use the standalone HTML for better compatibility
    html_to_embed = create_standalone_html()
    
    st.markdown('<div class="embed-container">', unsafe_allow_html=True)
    st.components.v1.html(html_to_embed, height=1000, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
except Exception as e:
    st.error(f"Error embedding analyzer: {str(e)}")

# Fallback option
st.markdown("### 🔄 Alternative Options")
col1, col2 = st.columns(2)

with col1:
    if st.button("Open in New Tab", key="new_tab"):
        st.markdown("[Open Full Analyzer](https://kirti1001.github.io/ACTION_ANALYZER/)", unsafe_allow_html=True)

with col2:
    if st.button("View GitHub Repository", key="github"):
        st.markdown("[Visit GitHub Repo](https://github.com/kirti1001/ACTION_ANALYZER)", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
**Note**: For best experience with camera access and full functionality, use the 'Open in New Tab' option.
Some browser restrictions may apply to embedded content.
""")
