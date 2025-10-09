import streamlit as st
import base64
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="AI Critical Action Analyzer",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def read_html_file():
    """Read the HTML template file"""
    try:
        with open('index.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        # Fallback HTML if template not found
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Critical Action Analyzer</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    text-align: center; 
                    padding: 50px;
                }
            </style>
        </head>
        <body>
            <h1>🏋️ AI Critical Action Analyzer</h1>
            <p>HTML template file not found. Please ensure 'templates/index.html' exists.</p>
        </body>
        </html>
        """

def main():
    # Custom CSS to hide Streamlit elements and make it fullscreen
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full screen styling */
    .stApp {
        background: transparent;
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    /* Make iframe full screen */
    .fullscreen-iframe {
        width: 100%;
        height: 100vh;
        border: none;
        position: fixed;
        top: 0;
        left: 0;
    }
    
    /* Control panel styling */
    .control-panel {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Read HTML content
    html_content = read_html_file()
    
    # Encode HTML to base64 for iframe
    html_base64 = base64.b64encode(html_content.encode()).decode()
    
    # Create iframe with HTML content
    iframe_html = f"""
    <iframe class="fullscreen-iframe" src="data:text/html;base64,{html_base64}"></iframe>
    """
    
    # Display the HTML app
    st.markdown(iframe_html, unsafe_allow_html=True)
    
    # Control panel (floating on top)
    with st.container():
        st.markdown("""
        <div class="control-panel">
            <h3>🎮 Controls</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Floating control panel using Streamlit
        col1, col2, col3 = st.columns([1,1,1])
        
        with col1:
            if st.button("🔄 Restart App"):
                st.rerun()
        
        with col2:
            if st.button("📊 View Data"):
                st.sidebar.info("Data logging would appear here")
        
        with col3:
            if st.button("ℹ️ Help"):
                st.sidebar.markdown("""
                ### How to Use:
                1. Allow camera access
                2. Click 'Start Analysis'
                3. Perform your exercises
                4. View real-time metrics
                5. Generate AI report
                """)

if __name__ == "__main__":
    main()
