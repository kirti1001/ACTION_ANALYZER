import streamlit as st
import requests

st.set_page_config(
    page_title="AI Critical Action Analyzer",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_github_file(url):
    """Load file directly from GitHub raw content"""
    try:
        # Convert GitHub URL to raw content URL
        raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        response = requests.get(raw_url)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None

def load_local_file(filename):
    """Load file from local repository"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def main():
    # Try to load files from GitHub first, then locally
    css_content = load_github_file('https://github.com/kirti1001/ACTION_ANALYZER/blob/584a0fd790554b4635c2fb595d597e9dea6da6fb/index.css') or load_local_file('index.css')
    js_content = load_github_file('https://github.com/kirti1001/ACTION_ANALYZER/blob/0bd9e447e92fc4ddbf56f2b091dbf5d75469d30b/index.js') or load_local_file('index.js')
    html_content = load_local_file('https://github.com/kirti1001/ACTION_ANALYZER/blob/9ad751ca2ceed93bb16edc437e5ab0792c9637d3/index.html')
    
    if not all([html_content, css_content, js_content]):
        st.error("❌ Could not load all required files. Please ensure index.html, index.css, and index.js are in your repository.")
        
        # Show file status
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("index.html", "✅" if html_content else "❌")
        with col2:
            st.metric("index.css", "✅" if css_content else "❌") 
        with col3:
            st.metric("index.js", "✅" if js_content else "❌")
        return

    # Create final HTML by replacing Flask template with embedded CSS/JS
    final_html = html_content.replace(
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'index.css\') }}">',
        f'<style>{css_content}</style>'
    )
    
    # Add JavaScript
    final_html = final_html.replace('</body>', f'<script>{js_content}</script></body>')
    
    # Display the application
    st.components.v1.html(final_html, height=1200, scrolling=True)

if __name__ == "__main__":
    main()
