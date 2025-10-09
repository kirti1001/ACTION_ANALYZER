import streamlit as st
import requests  # For fetching raw HTML from GitHub if not local

# Page configuration for a beautiful, themed app
st.set_page_config(
    page_title="AI Critical Action Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beauty (AI-themed: blues, gradients, modern fonts)
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1e3a8a; /* Deep blue for AI theme */
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0ea5e9; /* Light blue accent */
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
    .fallback-btn:hover {
        background: linear-gradient(135deg, #dc2626, #b91c1c);
        color: white;
    }
    .sidebar .sidebar-content {
        background: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load index.html content
@st.cache_data(ttl=3600)  # Cache for 1 hour to avoid repeated fetches
def load_html_content():
    try:
        # Option 1: Load from local file (if in the same repo for Streamlit Cloud deployment)
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Option 2: Fallback to fetch raw from GitHub (update your repo/commit SHA if needed)
        github_raw_url = "https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/main/index.html"  # Update branch/commit if needed
        response = requests.get(github_raw_url)
        response.raise_for_status()
        return response.text

# Sidebar for additional info (beautiful navigation)
with st.sidebar:
    st.title("📋 About the Analyzer")
    st.markdown("""
    ### Key Features
    - **Pose Detection**: Uses MediaPipe for real-time body landmark tracking.
    - **Metrics Analysis**: Posture, balance, symmetry, and motion scoring.
    - **AI Reports**: Generates professional insights via LLM (Puter.js integration).
    - **Offline Capable**: Works in browser with fallback local reports.
    
    ### Tech Stack
    - JavaScript + MediaPipe Pose
    - HTML5 Canvas for skeleton visualization
    - LLM for actionable recommendations
    
    ### Get Started
    The analyzer is embedded below. Grant camera access when prompted!
    If embedding has issues (e.g., camera), use the fallback button.
    """)
    
    # Sidebar expander for quick tips
    with st.expander("💡 Quick Tips"):
        st.markdown("""
        - Stand in good lighting and center yourself in the frame.
        - Select analysis duration (3-30 seconds).
        - Perform actions like stretches or walks for best results.
        - View reports in the modal after analysis.
        - For full screen: Use the fallback button to open in a new tab.
        """)

# Main content: Beautiful header and description
st.markdown('<h1 class="main-header">🤖 AI Based Critical Action Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Unlock insights into your posture, balance, and movement with AI-powered pose analysis. Stay balanced, stay active! 💪</p>', unsafe_allow_html=True)

# Two-column layout for features (beautiful cards)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="feature-box">🔍 **Real-Time Pose Tracking**<br>Detect 33 body landmarks with high accuracy using MediaPipe. Visualize your skeleton overlay in real-time.</div>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="feature-box">📊 **Smart Metrics & Reports**<br>Get scores for posture (alignment), balance (stability), symmetry (limb differences), and motion (smoothness). AI generates personalized recommendations.</div>', unsafe_allow_html=True)

# Row for more features
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="feature-box">⚡ **Efficient & Mobile-Friendly**<br>Optimized for desktops and mobiles. Samples at 2 FPS for quick analysis without lag.</div>', unsafe_allow_html=True)
    
with col4:
    st.markdown('<div class="feature-box">🛡️ **Privacy First**<br>Everything runs in your browser—no data sent to servers unless you choose backend mode.</div>', unsafe_allow_html=True)

# Separator
st.divider()

# Load and embed the index.html as a template
st.markdown("### 🚀 Launching the Analyzer...")
html_content = load_html_content()

# Embed the HTML using st.components.v1.html (renders as an iframe-like component)
# Height=1000px for full view; adjust based on your HTML layout
st.markdown('<div class="embed-container">', unsafe_allow_html=True)
components_html = st.components.v1.html(
    html_content,
    height=1000,
    scrolling=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Fallback button if embedding fails (e.g., JS/camera issues)
st.markdown("### 🔄 Fallback: Open in Full Browser Tab")
if st.button("Open Analyzer in New Tab", key="fallback_open", help="Bypasses embedding for full camera/JS support"):
    st.success("Opening the full analyzer... Click the link if it doesn't auto-open.")
    st.markdown(f"""
        <script>
        window.open('https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/main/index.html', '_blank');
        </script>
    """, unsafe_allow_html=True)
    st.markdown(f"[Direct Link to Analyzer](https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/main/index.html)")

# Footer with additional info
st.markdown("---")
st.markdown("""
### 🌟 Why Use This Analyzer?
This tool is designed for fitness enthusiasts, physiotherapists, and anyone interested in biomechanics. It provides encouraging, data-driven feedback to improve your daily movements and prevent injuries.

**Built with ❤️ using Streamlit for the landing/integration and your custom HTML/JS for the core analyzer.**

**Deployment Notes**:
- Embedded via Streamlit Components (JS runs in sandbox).
- If camera/pose detection doesn't work in embed, use the fallback button.
- For customizations or issues, check the [GitHub Repo](https://github.com/kirti1001/ACTION_ANALYZER).

""")

# Hide Streamlit menu and footer for a cleaner look
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
