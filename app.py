import streamlit as st

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
    .go-to-app-btn {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        font-size: 1.2rem;
        padding: 1rem 2rem;
        border-radius: 50px;
        border: none;
        width: 100%;
        height: 60px;
    }
    .go-to-app-btn:hover {
        background: linear-gradient(135deg, #059669, #047857);
        color: white;
    }
    .sidebar .sidebar-content {
        background: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

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
    Click "Go to App" below to launch the analyzer. Ensure camera access is granted!
    """)
    
    # Sidebar expander for quick tips
    with st.expander("💡 Quick Tips"):
        st.markdown("""
        - Stand in good lighting and center yourself in the frame.
        - Select analysis duration (3-30 seconds).
        - Perform actions like stretches or walks for best results.
        - View reports in the modal after analysis.
        """)

# Main content: Beautiful header and description
st.markdown('<h1 class="main-header">🤖 AI Based Critical Action Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Unlock insights into your posture, balance, and movement with AI-powered pose analysis. Stay balanced, stay active! 💪</p>', unsafe_allow_html=True)

# Two-column layout for features (beautiful cards)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="feature-box">🔍 **Real-Time Pose Tracking**<br>Detect 33 body landmarks with high accuracy using MediaPipe. Visualize your skeleton overlay in real-time.</div>', unsafe_allow_html=True)
    
with col2:
    st.markdown('<div class="feature-box">📊 **Smart Metrics & Reports**<br>Get scores for posture (alignment), balance (stability), symmetry (limb equality), and motion (smoothness). AI generates personalized recommendations.</div>', unsafe_allow_html=True)

# Row for more features
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="feature-box">⚡ **Efficient & Mobile-Friendly**<br>Optimized for desktops and mobiles. Samples at 2 FPS for quick analysis without lag.</div>', unsafe_allow_html=True)
    
with col4:
    st.markdown('<div class="feature-box">🛡️ **Privacy First**<br>Everything runs in your browser—no data sent to servers unless you choose backend mode.</div>', unsafe_allow_html=True)

# Separator
st.divider()

# Main button: "Go to App"
st.markdown("### Ready to Analyze? Launch the App Now!")
if st.button("🚀 Go to App", key="go_to_app", help="Opens the full analyzer in a new tab"):
    # Option 1: Open in new tab (recommended for full JS/camera functionality)
    st.success("Opening the AI Analyzer... If it doesn't open, click [here](https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/9ad751ca2ceed93bb16edc437e5ab0792c9637d3/index.html) to view directly.")
    st.markdown("""
        <script>
        window.open('https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/9ad751ca2ceed93bb16edc437e5ab0792c9637d3/index.html', '_blank');
        </script>
    """, unsafe_allow_html=True)
    
    # Optional: Embed iframe below the button (uncomment if you want to try embedding)
    # Note: May not work perfectly due to JS/camera restrictions in iframes
    # st.markdown("""
    #     <iframe src="https://raw.githubusercontent.com/kirti1001/ACTION_ANALYZER/9ad751ca2ceed93bb16edc437e5ab0792c9637d3/index.html" 
    #             width="100%" height="800px" style="border: 1px solid #ddd; border-radius: 10px;"></iframe>
    # """, unsafe_allow_html=True)

# Footer with additional info
st.markdown("---")
st.markdown("""
### 🌟 Why Use This Analyzer?
This tool is designed for fitness enthusiasts, physiotherapists, and anyone interested in biomechanics. It provides encouraging, data-driven feedback to improve your daily movements and prevent injuries.

**Built with ❤️ using Streamlit for the landing page and your custom HTML/JS for the core analyzer.**

If you have the `index.html`, JS, and CSS files locally:
1. Save them in a folder.
2. Open `index.html` in a modern browser (Chrome/Firefox recommended).
3. Grant camera permissions and start analyzing!

For issues or customizations, check the [GitHub Repo](https://github.com/kirti1001/ACTION_ANALYZER).
""")

# Hide Streamlit menu and footer for a cleaner look
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
