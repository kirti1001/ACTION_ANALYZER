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
    * {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

:root {
  --primary-gradient: linear-gradient(135deg, #6e8efb, #a777e3);
  --dark-bg: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --text-primary: #fff;
  --text-secondary: rgba(255, 255, 255, 0.8);
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
  --border-radius: 16px;
  --transition: all 0.3s ease;
}

body {
  background: var(--dark-bg);
  color: var(--text-primary);
  min-height: 100vh;
  overflow-x: hidden;
  padding-top: 80px;
}

.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  border: 1px solid var(--glass-border);
  padding: var(--spacing-md);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: var(--transition);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: var(--primary-gradient);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5d7df0, #9266d6);
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-header h2 {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  margin-bottom: var(--spacing-sm);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-header p {
  font-size: clamp(1rem, 2.5vw, 1.1rem);
  opacity: 0.8;
  max-width: min(600px, 90%);
  margin: 0 auto;
  line-height: 1.6;
}

/* ========== NAVIGATION ========== */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 15px 5%;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-container {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  font-weight: 700;
  z-index: 1001;
}

.nav-logo i {
  color: #a777e3;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: clamp(15px, 2vw, 30px);
  transition: var(--transition);
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: var(--transition);
  padding: 8px 15px;
  border-radius: 8px;
  font-size: clamp(0.9rem, 1.5vw, 1rem);
}

.nav-link:hover, .nav-link.active {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.1);
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: clamp(10px, 1.5vw, 15px);
}

.nav-auth .btn {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  transition: var(--transition);
  font-size: clamp(0.8rem, 1.5vw, 0.9rem);
}

.nav-auth .btn-login {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-auth .btn-login:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
}

.nav-auth .btn-signup {
  background: var(--primary-gradient);
  color: var(--text-primary);
  border: none;
}

.nav-auth .btn-signup:hover {
  background: linear-gradient(135deg, #5d7df0, #9266d6);
  box-shadow: 0 4px 15px rgba(167, 119, 227, 0.4);
}

/* Fixed Dropdown Styles */
.areas-dropdown {
  position: relative;
}

.areas-dropdown .nav-link {
  display: flex;
  align-items: center;
  gap: 5px;
}

.dropdown-content {
  display: block;
  position: absolute;
  top: 100%;
  left: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  min-width: 220px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 1000;
  margin-top: 15px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: var(--transition);
}

.areas-dropdown:hover .dropdown-content {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-gap {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  height: 15px;
}

.dropdown-content a {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  color: #333;
  text-decoration: none;
  transition: var(--transition);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.dropdown-content a i {
  margin-right: 12px;
  color: #6e8efb;
  width: 20px;
  text-align: center;
}

.dropdown-content a:hover {
  background: var(--primary-gradient);
  color: #fff;
}

.dropdown-content a:hover i {
  color: #fff;
}

.dropdown-content a:last-child {
  border-bottom: none;
}

/* Mobile Menu Button */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 30px;
  height: 30px;
  cursor: pointer;
  z-index: 1001;
}

.mobile-menu-btn i {
  font-size: 24px;
  color: #fff;
  transition: var(--transition);
}

/* Mobile auth buttons */
.mobile-auth {
  display: none;
  flex-direction: column;
  padding: 20px;
  gap: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 15px;
  width: 100%;
}

.mobile-auth .btn {
  width: 100%;
  text-align: center;
  justify-content: center;
}

/* ========== HERO SECTION ========== */
.hero {
  padding: clamp(50px, 8vw, 80px) 5% clamp(50px, 8vw, 70px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: clamp(20px, 4vw, 40px);
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
}

.hero-content {
  flex: 1;
  min-width: min(100%, 600px);
}

.hero-content h1 {
  font-size: clamp(2rem, 6vw, 3.5rem);
  margin-bottom: clamp(15px, 3vw, 20px);
  line-height: 1.2;
}

.hero-content p {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  margin-bottom: clamp(20px, 4vw, 30px);
  opacity: 0.9;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.hero-visual {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: min(100%, 300px);
}

.visual-container {
  width: min(100%, 300px);
  height: min(100%, 300px);
  aspect-ratio: 1/1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(110, 142, 251, 0.5);
  animation: pulse 3s infinite;
}

.delay-1 {
  animation-delay: 1s;
}

.delay-2 {
  animation-delay: 2s;
}

.visual-container i {
  font-size: clamp(4rem, 15vw, 8rem);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  70% {
    transform: scale(1.2);
    opacity: 0;
  }
  100% {
    transform: scale(0.8);
    opacity: 0;
  }
}

/* Time Selection Section */
.time-selection-section {
  padding: 3rem 2rem;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  margin: 2rem auto;
  max-width: 1200px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.time-selection-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  flex-wrap: wrap;
}

.time-slider-container {
  flex: 1;
  min-width: 300px;
}

.time-slider {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #4a6bff, #8a2be2);
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.time-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4a6bff;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 10px rgba(74, 107, 255, 0.4);
}

.time-slider::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4a6bff;
  cursor: pointer;
  border: 3px solid white;
  box-shadow: 0 2px 10px rgba(74, 107, 255, 0.4);
}

.time-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.time-display {
  text-align: center;
  min-width: 200px;
}

.time-value {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #4a6bff, #8a2be2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.time-description {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* Report Section */
.report-section {
  margin-top: 2rem;
  padding: 2rem;
  background: rgba(74, 107, 255, 0.1);
  border-radius: 15px;
  border: 1px solid rgba(74, 107, 255, 0.3);
  text-align: center;
}

.report-container {
  max-width: 400px;
  margin: 0 auto;
}

.btn-report {
  background: linear-gradient(135deg, #4a6bff, #8a2be2);
  color: white;
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(74, 107, 255, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-report:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 107, 255, 0.4);
}

.btn-report:active {
  transform: translateY(0);
}

.report-description {
  margin-top: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .time-selection-container {
    flex-direction: column;
    text-align: center;
  }
  
  .time-slider-container {
    min-width: 100%;
  }
  
  .time-value {
    font-size: 2rem;
  }
}


/* ========== MAIN CONTENT ========== */
.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.analysis-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 400px), 1fr));
  gap: clamp(20px, 3vw, 30px);
  margin-bottom: clamp(40px, 6vw, 60px);
}

/* Camera Card Styles */
.camera-card, .skeleton-card {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  border: 1px solid var(--glass-border);
  padding: var(--spacing-md);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.camera-card .card-header, .skeleton-card .card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  flex-wrap: wrap;
  gap: 10px;
}

.camera-card .card-header h3, .skeleton-card .card-header h3 {
  font-size: clamp(1.2rem, 3vw, 1.5rem);
}

.camera-indicator, .skeleton-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.indicator-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ff4757;
  transition: var(--transition);
}

.indicator-dot.active {
  background: #2ed573;
}

.camera-container, .skeleton-container {
  position: relative;
  width: 100%;
  height: min(60vw, 400px);
  border-radius: 12px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
}

.input_video, .output_canvas, #skeleton-canvas {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.output_canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.camera-overlay, .skeleton-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: clamp(2rem, 8vw, 3rem);
  transition: var(--transition);
}

.camera-overlay i, .skeleton-overlay i {
  margin-bottom: 15px;
}

.camera-overlay.hidden, .skeleton-overlay.hidden {
  opacity: 0;
  pointer-events: none;
}

.camera-controls, .skeleton-controls {
  display: flex;
  gap: 10px;
  margin-top: var(--spacing-md);
  flex-wrap: wrap;
  justify-content: center;
}

.skeleton-overlay p {
  margin-top: 15px;
  font-size: clamp(1rem, 3vw, 1.2rem);
  text-align: center;
  padding: 0 10px;
}

.skeleton-info {
  margin-top: var(--spacing-md);
}

.skeleton-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: clamp(10px, 2vw, 15px);
}

.stat {
  text-align: center;
  padding: 10px;
}

.stat-label {
  display: block;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  opacity: 0.8;
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  font-weight: 700;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: clamp(15px, 3vw, 25px);
  margin-bottom: clamp(40px, 6vw, 60px);
}

.stat-card {
  padding: clamp(15px, 3vw, 25px);
}

.stat-icon {
  font-size: clamp(2rem, 5vw, 2.5rem);
  margin-bottom: clamp(10px, 2vw, 15px);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-info h3 {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  margin-bottom: clamp(8px, 1.5vw, 10px);
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  margin-top: 5px;
  color: #2ed573;
}

.stat-progress {
  margin-top: clamp(10px, 2vw, 15px);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary-gradient);
  border-radius: 4px;
  width: 0%;
  transition: width 1s ease;
}

.progress-label {
  font-size: clamp(0.7rem, 1.8vw, 0.8rem);
  margin-top: 5px;
  opacity: 0.7;
}

/* Areas Section */
.areas-section {
  padding: clamp(50px, 8vw, 80px) 0;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin: clamp(30px, 5vw, 40px) 0;
}

.areas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
  gap: clamp(20px, 3vw, 25px);
  margin-top: clamp(30px, 5vw, 40px);
  padding: 0 20px;
}

.area-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius);
  padding: clamp(20px, 4vw, 30px);
  transition: var(--transition);
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.area-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(110, 142, 251, 0.1), rgba(167, 119, 227, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.area-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  border-color: rgba(110, 142, 251, 0.3);
}

.area-card:hover::before {
  opacity: 1;
}

.area-card .card-icon {
  width: clamp(50px, 10vw, 70px);
  height: clamp(50px, 10vw, 70px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: clamp(15px, 3vw, 20px);
  font-size: clamp(20px, 4vw, 28px);
  background: var(--primary-gradient);
  color: #fff;
}

.area-card h3 {
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  margin-bottom: clamp(10px, 2vw, 15px);
  color: #fff;
}

.area-card p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: clamp(15px, 3vw, 20px);
  line-height: 1.6;
  font-size: clamp(0.9rem, 2vw, 1rem);
}

.area-card .card-link {
  display: inline-flex;
  align-items: center;
  color: #6e8efb;
  text-decoration: none;
  font-weight: 600;
  transition: var(--transition);
  font-size: clamp(0.9rem, 2vw, 1rem);
}

.area-card .card-link i {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.area-card:hover .card-link {
  color: #a777e3;
}

.area-card:hover .card-link i {
  transform: translateX(5px);
}

/* Footer */
.footer {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  padding: clamp(40px, 6vw, 60px) 5% clamp(20px, 4vw, 30px);
  margin-top: clamp(50px, 8vw, 80px);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  gap: clamp(25px, 4vw, 40px);
  margin-bottom: clamp(30px, 5vw, 40px);
}

.footer-section h4 {
  font-size: clamp(1.1rem, 2.5vw, 1.3rem);
  margin-bottom: clamp(15px, 3vw, 20px);
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-section p {
  margin-bottom: clamp(15px, 3vw, 20px);
  opacity: 0.8;
  line-height: 1.6;
  font-size: clamp(0.9rem, 2vw, 1rem);
}

.footer-badges {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.tech-badge {
  padding: 5px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  font-size: clamp(0.7rem, 1.8vw, 0.8rem);
}

.footer-section a {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  margin-bottom: clamp(8px, 1.5vw, 12px);
  transition: var(--transition);
  font-size: clamp(0.9rem, 2vw, 1rem);
}

.footer-section a:hover {
  color: white;
  transform: translateX(5px);
}

.subscribe-form {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  flex-wrap: wrap;
}

.subscribe-form input {
  flex: 1;
  min-width: 200px;
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: clamp(0.9rem, 2vw, 1rem);
}

.subscribe-form input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.btn-sm {
  padding: 8px 15px;
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
}

.footer-bottom {
  text-align: center;
  padding-top: clamp(20px, 4vw, 30px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  opacity: 0.7;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
}

/* ========== RESPONSIVE BREAKPOINTS ========== */
@media (max-width: 1200px) {
  .analysis-content {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 992px) {
  body {
    padding-top: 70px;
  }
  
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 50px 5% 50px;
  }
  
  .hero-actions {
    justify-content: center;
  }
  
  .mobile-menu-btn {
    display: flex;
    z-index: 1002;
  }
  
  .nav-links {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: rgba(0, 0, 0, 0.98);
    backdrop-filter: blur(15px);
    flex-direction: column;
    padding: 100px 5% 30px;
    gap: 15px;
    transform: translateX(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    overflow-y: auto;
  }
  
  .nav-links.active {
    transform: translateX(0);
    opacity: 1;
    visibility: visible;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }
  
  .nav-auth {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 15px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .nav-auth .btn {
    width: 100%;
    text-align: center;
    justify-content: center;
  }
  
  .mobile-auth {
    display: none;
  }
  
  .nav-link {
    padding: 15px 20px;
    border-radius: 10px;
    font-size: 1.1rem;
    width: 100%;
    text-align: left;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    margin-bottom: 5px;
  }
  
  .areas-dropdown {
    width: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .areas-dropdown .nav-link {
    width: 100%;
    justify-content: space-between;
  }
  
  .dropdown-content {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    display: none;
    background: rgba(40, 40, 40, 0.8);
    margin: 10px 0 0 0;
    box-shadow: none;
    width: 100%;
    min-width: auto;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease;
    border-radius: 10px;
  }
  
  .areas-dropdown.active .dropdown-content {
    display: block;
    max-height: 500px;
  }
  
  .dropdown-content a {
    color: rgba(255, 255, 255, 0.9);
    border-bottom-color: rgba(255, 255, 255, 0.1);
    padding: 15px 20px 15px 40px;
    font-size: 1rem;
  }
  
  .dropdown-gap {
    display: none;
  }
  
  .nav-links::before {
    content: 'Menu';
    position: absolute;
    top: 30px;
    left: 5%;
    font-size: 1.5rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .nav-logo {
    z-index: 1002;
    position: relative;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .skeleton-stats {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .hero-content h1 {
    font-size: 2.5rem;
  }
  
  .visual-container {
    width: 200px;
    height: 200px;
  }
  
  .visual-container i {
    font-size: 5rem;
  }
  
  .section-header h2 {
    font-size: 2rem;
  }
  
  .subscribe-form input {
    min-width: 100%;
  }
}

@media (max-width: 576px) {
  .navbar {
    padding: 12px 4%;
  }
  
  .nav-logo {
    font-size: 1.2rem;
  }
  
  .nav-logo i {
    font-size: 1.3rem;
  }
  
  .nav-links {
    padding: 90px 4% 30px;
  }
  
  body {
    padding-top: 64px;
  }
  
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .hero-actions .btn {
    width: 100%;
    justify-content: center;
  }
  
  .camera-controls, .skeleton-controls {
    flex-direction: column;
  }
  
  .camera-controls .btn, .skeleton-controls .btn {
    width: 100%;
    justify-content: center;
  }
  
  .dropdown-content a {
    padding: 12px 15px 12px 35px;
    font-size: 0.95rem;
  }
  
  .areas-grid {
    padding: 0 10px;
  }
}

@media (min-width: 993px) {
  .mobile-auth {
    display: none;
  }
  
  .mobile-menu-btn {
    display: none;
  }
}

/* Animation for smooth transitions */
.nav-links, .dropdown-content {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Prevent body scroll when menu is open */
body.menu-open {
  overflow: hidden;
  position: fixed;
  width: 100%;
}

/* Improved focus styles for accessibility */
button:focus-visible,
a:focus-visible,
input:focus-visible {
  outline: 2px solid #6e8efb;
  outline-offset: 2px;
}

/* Reduced motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}


/* ========== 1000px AND BELOW MOBILE VIEW - FULL WIDTH ========== */
/* ========== 1000px AND BELOW MOBILE VIEW - FULL WIDTH ========== */
@media (max-width: 1000px) {
  /* Body and Navigation Adjustments */
  body {
    padding-top: 70px;
  }

  /* Mobile Menu Button */
  .mobile-menu-btn {
    display: flex;
    z-index: 1003;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px;
    transition: all 0.3s ease;
    margin-right: 15px; /* Added distance between mobile button and login/signup */
  }

  .mobile-menu-btn:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .mobile-menu-btn.active {
    background: rgba(110, 142, 251, 0.3);
  }

  .mobile-menu-btn i {
    font-size: 24px;
    color: #fff;
    transition: all 0.3s ease;
  }

  .mobile-menu-btn.active i::before {
    content: '\f00d'; /* Close icon */
  }

  /* Navigation Links */
  .nav-links {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background: rgba(0, 0, 0, 0.98);
    backdrop-filter: blur(15px);
    flex-direction: column;
    padding: 100px 5% 30px;
    gap: 15px;
    transform: translateX(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1002;
    overflow-y: auto;
    box-shadow: 0 0 0 100vmax rgba(0, 0, 0, 0.8);
  }

  .nav-links.active {
    transform: translateX(0);
    opacity: 1;
    visibility: visible;
  }

  /* Modified Login/Signup Bar */
  .nav-auth {
    display: flex;
    flex-direction: column;
    width: 90%; /* Reduced from 100% to 80% */
    max-width: 400px; /* Added max-width */
    gap: 15px;
    margin: 20px auto 0; /* Changed to auto for centering */
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    align-self: center; /* Center the container */
  }

  .nav-auth .btn {
    width: 100%; /* Buttons fill the container */
    text-align: center;
    justify-content: center;
  }

  .nav-link {
    padding: 15px 20px;
    border-radius: 10px;
    font-size: 1.1rem;
    width: 100%;
    text-align: left;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    margin-bottom: 5px;
    transition: all 0.3s ease;
  }

  .nav-link:hover {
    background: rgba(110, 142, 251, 0.2);
    transform: translateX(5px);
  }

  /* Dropdown Menu */
  .areas-dropdown {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .areas-dropdown .nav-link {
    width: 100%;
    justify-content: space-between;
  }

  .dropdown-content {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    display: none;
    background: rgba(40, 40, 40, 0.8);
    margin: 10px 0 0 0;
    box-shadow: none;
    width: 100%;
    min-width: auto;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease;
    border-radius: 10px;
  }

  .areas-dropdown.active .dropdown-content {
    display: block;
    max-height: 500px;
  }

  .dropdown-content a {
    color: rgba(255, 255, 255, 0.9);
    border-bottom-color: rgba(255, 255, 255, 0.1);
    padding: 15px 20px 15px 40px;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  .dropdown-content a:hover {
    background: rgba(110, 142, 251, 0.3);
    padding-left: 45px;
  }

  .dropdown-gap {
    display: none;
  }

  .nav-links::before {
    content: 'Menu';
    position: absolute;
    top: 30px;
    left: 5%;
    font-size: 1.5rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .nav-logo {
    z-index: 1002;
    position: relative;
  }

  /* Hero Section - Full Width */
  .hero {
    flex-direction: column;
    text-align: center;
    padding: 50px 5% 50px;
    width: 100%;
  }

  .hero-content {
    min-width: 100%;
    width: 100%;
  }

  .hero-actions {
    justify-content: center;
    flex-direction: column;
    width: 100%;
  }

  .hero-actions .btn {
    width: 100%;
    justify-content: center;
  }

  /* Specialized Areas Section - Full Width */
  .areas-section {
    padding: 50px 0;
    width: 100%;
  }

  .areas-container {
    width: 100%;
    padding: 0 5%;
  }

  .areas-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-top: 30px;
    width: 100%;
  }

  .area-card {
    width: 100%;
    transition: all 0.3s ease;
  }

  /* Stats Grid - Full Width */
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
    width: 100%;
  }

  .stat-card {
    width: 100%;
  }

  /* Analysis Content - Full Width */
  .analysis-content {
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
    width: 100%;
  }

  .camera-card, .skeleton-card {
    width: 100%;
  }

  /* Camera Controls */
  .camera-controls, .skeleton-controls {
    flex-direction: column;
    gap: 10px;
    width: 100%;
  }

  .camera-controls .btn, .skeleton-controls .btn {
    width: 100%;
    justify-content: center;
  }

  /* Skeleton Stats */
  /* .skeleton-stats {
    grid-template-columns: 1fr;
    gap: 15px;
    width: 100%;
  } */

   .skeleton-stats {
    display: flex;
    flex-direction: row;
    gap: 270px;
    width: 100%;
    overflow-x: auto;
    padding-bottom: 10px; /* Space for scrollbar */
    -webkit-overflow-scrolling: touch; /* Smooth scrolling on iOS */
  }

  .skeleton-stats .stat-card {
    flex: 0 0 auto;
    min-width: 200px; /* Minimum width for each stat card */
    width: auto; /* Override the 100% width */
  }


  /* AI-Powered Critical Action Analysis Heading Adjustment */
  .hero-content {
    margin-top: 40px; /* Added space to prevent hiding behind navbar */
  }

  /* Footer - 2x2 Grid Layout */
  .footer {
    padding: 40px 0 20px;
    margin-top: 50px;
    width: 100%;
  }

  .footer-container {
    width: 100%;
    padding: 0 5%;
  }

  .footer-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 2 columns */
    grid-template-rows: auto auto; /* 2 rows */
    gap: 30px;
    margin-bottom: 30px;
    width: 100%;
  }

  .footer-section {
    text-align: left;
    padding: 0 10px;
  }

  .footer-section h4 {
    font-size: 1.1rem;
    margin-bottom: 15px;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .footer-section p {
    margin-bottom: 15px;
    line-height: 1.6;
    font-size: 0.9rem;
  }

  .footer-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .tech-badge {
    padding: 5px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    font-size: 0.8rem;
  }

  .footer-section a {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: var(--transition);
    font-size: 0.9rem;
  }

  .footer-section a:hover {
    color: white;
    transform: translateX(5px);
  }

  .footer-section a i {
    margin-right: 10px;
    font-size: 1rem;
  }

  .subscribe-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 15px;
  }

  .subscribe-form input {
    width: 100%;
    padding: 12px 15px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }

  .subscribe-form input::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  .subscribe-form .btn {
    width: 100%;
    padding: 12px 20px;
  }

  .footer-bottom {
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 0.9rem;
    text-align: center;
    width: 100%;
  }

  /* Body Scroll Lock */
  body.menu-open {
    overflow: hidden;
    position: fixed;
    width: 100%;
  }
}

/* Small Screen Adjustments (576px and below) */
@media (max-width: 576px) {
  .navbar {
    padding: 12px 4%;
  }

  .nav-logo {
    font-size: 1.2rem;
  }

  .nav-logo i {
    font-size: 1.3rem;
  }

  .nav-links {
    padding: 90px 4% 30px;
  }

  body {
    padding-top: 64px;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-content p {
    font-size: 1rem;
  }

  .dropdown-content a {
    padding: 12px 15px 12px 35px;
    font-size: 0.95rem;
  }
  
  /* Footer adjustments for very small screens */
  .footer-content {
    grid-template-columns: 1fr; /* Single column for very small screens */
    gap: 20px;
  }
  
  /* Further reduce login/signup bar for very small screens */
  .nav-auth {
    width: 90%; /* Slightly wider on very small screens */
    max-width: 280px; /* Slightly smaller max-width */
  }
}



/* ========== REPORT SELECTION COMPONENT ========== */

/* Report Modal Styles */
.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  animation: fadeIn 0.3s ease-in-out;
}

.modal-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: 2% auto;
  padding: 0;
  border-radius: 15px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease-out;
}

.modal-header {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(10px);
}

.modal-header h2 {
  margin: 0;
  color: white;
  font-size: 1.5em;
  font-weight: 600;
}

.close {
  color: white;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close:hover {
  color: #ff6b6b;
}

.modal-body {
  padding: 30px;
  background: white;
  max-height: 60vh;
  overflow-y: auto;
}

.report-content {
  line-height: 1.6;
  color: #333;
  font-size: 14px;
  white-space: pre-line;
}

/* Beautiful report formatting */
.report-content h3 {
  color: #4a5568;
  border-bottom: 2px solid #667eea;
  padding-bottom: 8px;
  margin-top: 25px;
  margin-bottom: 15px;
}

.report-content ul, .report-content ol {
  margin: 15px 0;
  padding-left: 20px;
}

.report-content li {
  margin-bottom: 8px;
}

.report-content strong {
  color: #2d3748;
  font-weight: 600;
}

.report-content .score {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  margin: 20px 0;
  font-size: 1.2em;
  font-weight: bold;
}

.modal-footer {
  background: rgba(255, 255, 255, 0.1);
  padding: 20px 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  backdrop-filter: blur(10px);
}

.btn-download {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-download:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
}

.btn-close {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* Report Section Styles */
.report-section {
  margin: 30px 0;
  text-align: center;
}

.report-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.btn-report {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 15px 30px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.btn-report:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 255, 255, 0.2);
}

.report-description {
  color: rgba(255, 255, 255, 0.9);
  margin-top: 15px;
  font-size: 0.9em;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { 
    opacity: 0;
    transform: translateY(-50px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 5% auto;
  }
  
  .modal-header {
    padding: 15px 20px;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .modal-footer {
    padding: 15px 20px;
    flex-direction: column;
  }
}
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
            const DEBUG = true;

function log(...args) {
  if (DEBUG) console.log('[AI Analyzer]', ...args);
}

function error(...args) {
  console.error('[AI Analyzer]', ...args);
}

// Constants
const FPS_CAP = 20; // Pose ~30 FPS
const SAMPLING_FPS = 2; // Sample 2/sec
const VISIBLE_THRESHOLD = 0.4;
const ANALYSIS_MAX_SAMPLES = 100;
const RETRY_ATTEMPTS = 3;
const CONNECTIONS = [
  [11,12],[11,13],[13,15],[12,14],[14,16],
  [23,24],[23,25],[25,27],[24,26],[26,28],
  [0,23],[0,24],[11,23],[11,12],[12,24]
];
let report = null;

// Throttle for efficiency
function throttle(fn, limit) {
  let lastCall = 0;
  return function(...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      return fn(...args);
    }
  };
}

// Batch DOM updates with RAF
let rafId = null;
function batchUpdate(fn) {
  if (rafId) cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(() => {
    fn();
    rafId = null;
  });
}

// Metrics (main thread for simplicity/reliability)
function calculateMetrics(landmarks, previous) {
  if (!landmarks || landmarks.length < 1) return { posture: 0, balance: 0, symmetry: 0, motion: 0 };

  const leftShoulder = landmarks[11], rightShoulder = landmarks[12];
  const leftHip = landmarks[23], rightHip = landmarks[24];
  const leftKnee = landmarks[25], rightKnee = landmarks[26];

  // Posture
  const shoulderVec = { x: rightShoulder.x - leftShoulder.x, y: rightShoulder.y - leftShoulder.y };
  const hipVec = { x: rightHip.x - leftHip.x, y: rightHip.y - leftHip.y };
  const magS = Math.hypot(shoulderVec.x, shoulderVec.y);
  const magH = Math.hypot(hipVec.x, hipVec.y);
  let postureAngle = 0;
  if (magS > 0 && magH > 0) {
    const dot = shoulderVec.x * hipVec.x + shoulderVec.y * hipVec.y;
    postureAngle = Math.acos(Math.max(-1, Math.min(1, dot / (magS * magH)))) * 180 / Math.PI;
  }
  const postureScore = Math.max(0, 100 - Math.abs(postureAngle - 180));

  // Balance
  const hipDiff = Math.abs(leftHip.y - rightHip.y);
  const kneeDiff = Math.abs(leftKnee.y - rightKnee.y);
  const balanceScore = Math.max(0, 100 - (hipDiff + kneeDiff) * 1000);

  // Symmetry
  const leftArm = Math.hypot(leftShoulder.x - landmarks[13].x, leftShoulder.y - landmarks[13].y);
  const rightArm = Math.hypot(rightShoulder.x - landmarks[14].x, rightShoulder.y - landmarks[14].y);
  const leftLeg = Math.hypot(leftHip.x - leftKnee.x, leftHip.y - leftKnee.y);
  const rightLeg = Math.hypot(rightHip.x - rightKnee.x, rightHip.y - rightKnee.y);
  const symDiff = Math.abs(leftArm - rightArm) + Math.abs(leftLeg - rightLeg);
  const symmetryScore = Math.max(0, 100 - symDiff * 500);

  // Motion
  let motionScore = 100;
  if (previous) {
    const vel = Math.hypot(
      leftShoulder.x - previous[11].x, leftShoulder.y - previous[11].y,
      rightShoulder.x - previous[12].x, rightShoulder.y - previous[12].y
    ) * FPS_CAP;
    const variance = Math.abs(vel - (window.lastVel || 0));
    motionScore = Math.max(0, 100 - variance * 10);
    window.lastVel = vel;
  }

  return { posture: postureScore, balance: balanceScore, symmetry: symmetryScore, motion: motionScore };
}

// DOM Ready
document.addEventListener('DOMContentLoaded', async () => {
  if (typeof Pose === 'undefined' || typeof Camera === 'undefined') {
    error('Required libraries not loaded');
    alert('Libraries failed to load. Refresh page.');
    return;
  }
  log('Libraries loaded');

  // Core vars
  let pose, camera, video, canvas, ctx, skeletonCanvas, skeletonCtx;
  let isAnalyzing = false, frameData = [], sampleInterval, previousLandmarks = null, latestLandmarks = [], noPoseTimer = 0;
  let fpsCounter = { frames: 0, lastTime: 0 };
  window.lastVel = 0;
  const metricThrottle = throttle(() => calculateMetrics(latestLandmarks, previousLandmarks), 100);
  const updateSkeletonThrottle = throttle((landmarks) => {
    latestLandmarks = landmarks;
    if (skeletonCtx) updateSkeleton2D(landmarks);
  }, 100 / FPS_CAP);

  // Navbar (simplified, no errors)
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');
  const mobileAuth = document.querySelector('.mobile-auth');
  const areasDropdown = document.querySelector('.areas-dropdown');
  const body = document.body;

  function toggleMobileMenu() {
    const isOpen = navLinks.classList.toggle('active');
    mobileAuth.classList.toggle('active');
    body.classList.toggle('menu-open', isOpen);
    const icon = mobileMenuBtn.querySelector('i');
    icon.classList.toggle('fa-bars', !isOpen);
    icon.classList.toggle('fa-times', isOpen);
    if (!isOpen) areasDropdown?.classList.remove('active');
  }

  mobileMenuBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMobileMenu();
  });

  document.querySelector('.areas-dropdown .nav-link')?.addEventListener('click', (e) => {
    if (window.innerWidth <= 992) {
      e.preventDefault();
      e.stopPropagation();
      areasDropdown.classList.toggle('active');
    }
  });

  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 992) {
      if (areasDropdown?.classList.contains('active') && !areasDropdown.contains(e.target)) {
        areasDropdown.classList.remove('active');
      }
      if (navLinks.classList.contains('active') && !e.target.closest('.nav-container')) {
        toggleMobileMenu();
      }
    }
  });

  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 992) setTimeout(toggleMobileMenu, 300);
    });
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 992) {
      navLinks.classList.remove('active');
      mobileAuth.classList.remove('active');
      body.classList.remove('menu-open');
      areasDropdown?.classList.remove('active');
      mobileMenuBtn.querySelector('i').classList.add('fa-bars');
      mobileMenuBtn.querySelector('i').classList.remove('fa-times');
    }
    if (skeletonCanvas) {
      const rect = skeletonCanvas.getBoundingClientRect();
      skeletonCanvas.width = rect.width;
      skeletonCanvas.height = rect.height;
      if (skeletonCtx) {
        updateSkeleton2D(latestLandmarks);
      }
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && window.innerWidth <= 992) {
      if (areasDropdown?.classList.contains('active')) {
        areasDropdown.classList.remove('active');
      } else {
        toggleMobileMenu();
      }
    }
  });

  // Vanta (optional, no errors)
  if (window.innerWidth > 1000 && VANTA?.NET) {
    VANTA.NET({
      el: document.body,
      mouseControls: true,
      touchControls: false,
      gyroControls: false,
      minHeight: 200,
      minWidth: 300,
      scale: 1,
      scaleMobile: 0.8,
      color: 0x3f51b5,
      backgroundColor: 0x0,
      points: 20,
      maxDistance: 15,
      spacing: 12
    });
  }

  // Pose init (no errors)
  pose = new Pose({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.2/${file}`
  });
  pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.4,
    minTrackingConfidence: 0.4
  });
  pose.onResults(onPoseResults);
  log('Pose ready');

  // Skeleton init (2D canvas only - no Three.js)
  function initSkeleton() {
    const container = document.getElementById('skeleton-canvas');
    if (!container) return error('No skeleton canvas');

    skeletonCanvas = container;
    skeletonCtx = container.getContext('2d');
    
    // Set canvas size
    const rect = container.getBoundingClientRect();
    skeletonCanvas.width = rect.width;
    skeletonCanvas.height = rect.height;
    
    log('2D Skeleton canvas ready for landmarks');
    drawStaticHuman2D();
  }

  function drawStaticHuman2D() {
    if (!skeletonCtx) return;
    const w = skeletonCanvas.width, h = skeletonCanvas.height, cx = w / 2, cy = h / 2;
    
    // Clear canvas
    skeletonCtx.clearRect(0, 0, w, h);
    
    // Draw static human figure
    skeletonCtx.strokeStyle = '#00ff00';
    skeletonCtx.lineWidth = 2;
    skeletonCtx.fillStyle = '#00ff00';
    
    skeletonCtx.beginPath();
    // Head
    skeletonCtx.arc(cx, cy - 50, 20, 0, Math.PI * 2);
    // Body
    skeletonCtx.moveTo(cx, cy - 30); 
    skeletonCtx.lineTo(cx, cy + 50);
    // Arms
    skeletonCtx.moveTo(cx, cy - 10); 
    skeletonCtx.lineTo(cx - 40, cy + 10);
    skeletonCtx.moveTo(cx, cy - 10); 
    skeletonCtx.lineTo(cx + 40, cy + 10);
    // Legs
    skeletonCtx.moveTo(cx, cy + 50); 
    skeletonCtx.lineTo(cx - 30, cy + 100);
    skeletonCtx.moveTo(cx, cy + 50); 
    skeletonCtx.lineTo(cx + 30, cy + 100);
    skeletonCtx.stroke();
  }

  function updateSkeleton2D(landmarks) {
    if (!skeletonCtx || !skeletonCanvas) return;
    
    const w = skeletonCanvas.width, h = skeletonCanvas.height;
    
    // Clear canvas
    skeletonCtx.clearRect(0, 0, w, h);
    
    if (!landmarks || landmarks.length === 0) {
      drawStaticHuman2D();
      return;
    }

    // Draw connections (bones)
    skeletonCtx.strokeStyle = '#00ff00';
    skeletonCtx.lineWidth = 3;
    skeletonCtx.beginPath();
    
    CONNECTIONS.forEach(([i, j]) => {
      if (landmarks[i]?.visibility > VISIBLE_THRESHOLD && landmarks[j]?.visibility > VISIBLE_THRESHOLD) {
        const x1 = landmarks[i].x * w;
        const y1 = landmarks[i].y * h;
        const x2 = landmarks[j].x * w;
        const y2 = landmarks[j].y * h;
        
        skeletonCtx.moveTo(x1, y1);
        skeletonCtx.lineTo(x2, y2);
      }
    });
    skeletonCtx.stroke();

    // Draw landmarks (joints)
    skeletonCtx.fillStyle = '#ff0000';
    landmarks.forEach(lm => {
      if (lm.visibility > VISIBLE_THRESHOLD) {
        const x = lm.x * w;
        const y = lm.y * h;
        
        skeletonCtx.beginPath();
        skeletonCtx.arc(x, y, 4, 0, Math.PI * 2);
        skeletonCtx.fill();
      }
    });

    // Draw landmark numbers (optional - for debugging)
    if (DEBUG) {
      skeletonCtx.fillStyle = '#ffffff';
      skeletonCtx.font = '10px Arial';
      landmarks.forEach((lm, i) => {
        if (lm.visibility > VISIBLE_THRESHOLD) {
          const x = lm.x * w;
          const y = lm.y * h;
          skeletonCtx.fillText(i.toString(), x + 5, y - 5);
        }
      });
    }
  }

  // Pose results (no errors, clean feed)
  function onPoseResults(results) {
    if (!ctx || !canvas) return;
    ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);

    if (results.poseLandmarks) {
      const visibleCount = results.poseLandmarks.filter(lm => lm.visibility > VISIBLE_THRESHOLD).length;
      const avgConf = results.poseLandmarks.reduce((sum, lm) => sum + lm.visibility, 0) / 33 * 100;

      const now = performance.now();
      fpsCounter.frames++;
      if (now - fpsCounter.lastTime >= 1000) {
        fpsCounter.frames = Math.round(fpsCounter.frames * 1000 / (now - fpsCounter.lastTime));
        fpsCounter.lastTime = now;
      }

      batchUpdate(() => {
        const landmarksEl = document.getElementById('landmarks-count');
        const confEl = document.getElementById('confidence-score');
        const fpsEl = document.getElementById('frame-rate');
        if (landmarksEl) landmarksEl.textContent = visibleCount;
        if (confEl) confEl.textContent = `${avgConf.toFixed(1)}%`;
        if (fpsEl) fpsEl.textContent = `${fpsCounter.frames} FPS`;

        // Skeleton update (throttled, synced with pose)
        updateSkeletonThrottle(Array.from(results.poseLandmarks));

        // Metrics (only during analysis)
        if (isAnalyzing) {
          const metrics = calculateMetrics(results.poseLandmarks, previousLandmarks);
          updateMetricUI('posture', metrics.posture);
          updateMetricUI('balance', metrics.balance);
          updateMetricUI('symmetry', metrics.symmetry);
          updateMetricUI('motion', metrics.motion);
        }

        // Status indicators
        const overlayEl = document.getElementById('skeleton-overlay');
        const statusEl = document.querySelector('#skeleton-status');
        if (overlayEl) overlayEl.style.display = 'none';
        if (statusEl) statusEl.className = 'indicator-dot green';
      });

      noPoseTimer = 0;
      previousLandmarks = Array.from(results.poseLandmarks);
    } else {
      noPoseTimer++;
      if (noPoseTimer > 90 && isAnalyzing) { // ~3s at 30 FPS
        alert('No pose detected. Ensure you are visible and centered in frame.');
        noPoseTimer = 0;
      }
      batchUpdate(() => {
        const statusEl = document.querySelector('#skeleton-status');
        const overlayEl = document.getElementById('skeleton-overlay');
        if (statusEl) statusEl.className = 'indicator-dot red';
        if (overlayEl) overlayEl.style.display = 'block';
        updateSkeletonThrottle([]); // Clear skeleton
      });
    }
  }

  // Update Metric UI (dynamic, with trends)
  function updateMetricUI(type, score) {
    const scoreEl = document.getElementById(`${type}-score`);
    const progressEl = document.getElementById(`${type}-progress`);
    const trendEl = document.getElementById(`${type}-trend`);
    if (!scoreEl || !progressEl || !trendEl) return;

    const rounded = Math.round(Math.min(100, Math.max(0, score)));
    scoreEl.textContent = `${rounded}%`;
    progressEl.style.width = `${rounded}%`;

    // Trend
    const prev = parseInt(localStorage.getItem(`prev_${type}`) || '0');
    const diff = rounded - prev;
    const icon = diff > 0 ? 'fa-arrow-up' : diff < 0 ? 'fa-arrow-down' : 'fa-minus';
    const text = diff !== 0 ? `${Math.abs(diff)}% from last` : 'No previous data';
    trendEl.innerHTML = `<i class="fas ${icon}"></i> <span>${text}</span>`;
    localStorage.setItem(`prev_${type}`, rounded.toString());
  }

    // Sample frame (2/sec, sequential data for backend)
  function sampleFrame(second, frameIndex, landmarks) {
    if (frameData.length >= ANALYSIS_MAX_SAMPLES) return;

    const landmarkNames = [
      'nose','left_eye_inner','left_eye','left_eye_outer','right_eye_inner','right_eye','right_eye_outer',
      'left_ear','right_ear','mouth_left','mouth_right','left_shoulder','right_shoulder','left_elbow',
      'right_elbow','left_wrist','right_wrist','left_pinky','right_pinky','left_index','right_index',
      'left_thumb','right_thumb','left_hip','right_hip','left_knee','right_knee','left_ankle',
      'right_ankle','left_heel','right_heel','left_foot_index','right_foot_index'
    ];

    const visibleLandmarks = {};
    landmarks.forEach((lm, i) => {
      if (lm.visibility > VISIBLE_THRESHOLD) {
        visibleLandmarks[landmarkNames[i]] = { x: lm.x, y: lm.y, z: lm.z || 0, visibility: lm.visibility };
      }
    });

    const leftShoulder = landmarks[11], rightShoulder = landmarks[12], leftHip = landmarks[23], rightHip = landmarks[24];
    const features = {
      shoulder_pitch: Math.atan2(rightShoulder.y - leftShoulder.y, rightShoulder.x - leftShoulder.x) * 180 / Math.PI,
      torso_tilt: Math.atan2(rightHip.y - leftHip.y, rightHip.x - leftHip.x) * 180 / Math.PI,
      joint_velocity: previousLandmarks ? Math.hypot(
        leftShoulder.x - previousLandmarks[11].x, leftShoulder.y - previousLandmarks[11].y
      ) * SAMPLING_FPS : 0,
      step_symmetry: Math.abs((leftHip.x - rightHip.x) - (previousLandmarks ? (previousLandmarks[23].x - previousLandmarks[24].x) : 0)),
      quality_score: (Object.keys(visibleLandmarks).length / 33) * 100
    };

    const frameDataItem = {
      second,
      frameIndex,
      landmarks: visibleLandmarks,
      features
    };

    frameData.push(frameDataItem);
    log(`Sampled frame ${frameIndex}s${second} (${frameData.length}/${ANALYSIS_MAX_SAMPLES})`);

    // Optional backend send (no error if 404/offline)
    // if (typeof fetch !== 'undefined') {
    //   fetch('/', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ frame: frameDataItem, stage: 'sample' })
    //   }).catch(err => {
    //     if (DEBUG) error('Backend sample send failed (offline mode):', err);
    //   });
    // }
  }

  // Analysis timer (non-blocking, 2 FPS sampling)
  async function startAnalysisTimer(duration) {
    const totalSamples = Math.min(duration * SAMPLING_FPS, ANALYSIS_MAX_SAMPLES);
    let currentSecond = 1, samplesInSecond = 0;

    // Optional backend start (no error if 404)
    // if (typeof fetch !== 'undefined') {
    //   try {
    //     await fetch('/', {
    //       method: 'POST',
    //       headers: { 'Content-Type': 'application/json' },
    //       body: JSON.stringify({ duration, stage: 'start' })
    //     });
    //     log('Backend started');
    //   } catch (err) {
    //     if (DEBUG) error('Backend start failed (continuing offline):', err);
    //   }
    // }

    sampleInterval = setInterval(() => {
      if (!isAnalyzing || frameData.length >= totalSamples) {
        clearInterval(sampleInterval);
        finalizeAnalysis();
        return;
      }

      if (latestLandmarks.length > 3) {
        samplesInSecond++;
        sampleFrame(currentSecond, samplesInSecond, latestLandmarks);

        // Progress UI (dynamic)
        batchUpdate(() => {
          const progress = Math.min(100, (frameData.length / totalSamples) * 100);
          const progressEl = document.getElementById('analysis-progress');
          if (progressEl) progressEl.style.width = `${progress}%`;
        });

        if (samplesInSecond >= SAMPLING_FPS) {
          currentSecond++;
          samplesInSecond = 0;
        }
      }
    }, 1000 / SAMPLING_FPS);
  }

  // Finalize analysis (updated: Send to backend for LLM report)
async function finalizeAnalysis() {
  isAnalyzing = false;
  clearInterval(sampleInterval);
  stopCamera(); // Uncomment if you want auto-stop after analysis
  const analysisData = {
    metadata: {
      timestamp: new Date().toISOString(),
      duration: parseInt(document.getElementById('time-display')?.textContent || '5'),
      totalFrames: frameData.length
    },
    frames: frameData.slice(0, ANALYSIS_MAX_SAMPLES)
  };

  log('Analysis complete. Frames:', frameData.length);
  console.log('Full JSON Data:', JSON.stringify(analysisData, null, 2));

  

  // Use Puter.js for LLM processing (no backend needed)
  try {
    // Construct the same prompt you were using in the backend
    const prompt = `You are an expert in human movement analysis and biomechanics.
    Analyze the following pose detection data from a user's physical activity session (collected via MediaPipe Pose landmarks).

Data Summary:
- Duration: ${analysisData.metadata.duration} seconds
- Total Frames: ${analysisData.metadata.totalFrames}
- Timestamp: ${analysisData.metadata.timestamp}

Sample Frame Structure (showing landmarks and features for ${analysisData.frames.length} frames):
${JSON.stringify(analysisData.frames.slice(0, 5), null, 2)}  # First 5 frames as example; analyze all implicitly.

Key Features Across Frames (computed from landmarks):
- Landmarks: 33 body points (e.g., nose, shoulders, hips, knees) with x,y,z coordinates and visibility scores.
- Extracted Metrics: shoulder_pitch (degrees), torso_tilt (degrees), joint_velocity (px/s), step_symmetry (difference), quality_score (% visible landmarks).

Generate a comprehensive, professional movement report for the user. Structure it as follows:
1. **Summary**: Overview of session (e.g., overall posture quality, activity efficiency).
2. **Key Metrics**: Break down averages for posture (shoulder alignment), balance (hip/knee stability), symmetry (limb differences), motion (smoothness/velocity).
3. **Insights**: Analyze patterns (e.g., "High shoulder pitch suggests forward lean—potential back strain risk"). Reference specific data (e.g., avg shoulder_pitch: X°).
4. **Recommendations**: Personalized tips (e.g., "Strengthen core for better balance"). Flag risks (e.g., asymmetry >20% may indicate injury).
5. **Overall Score**: 0-100% efficiency rating.

Make it engaging, actionable. Use bullet points/tables for readability. Base analysis strictly on data—be positive and encouraging.`;

    // Use Puter.js AI instead of backend API call
    report = await puter.ai.chat(prompt, { model: "gpt-5-nano" });
    // Store the report and show the report section
    currentReport = report;
    const reportSection = document.getElementById('report-section');
    if (reportSection) {
      reportSection.style.display = 'block';
    }
    log('LLM Report generated successfully via Puter.js');

  } catch (err) {
    error('Puter.js AI failed:', err);
    log('Falling back to local report generation');
    // Fallback: Generate local report
    // report = generateReport();  // static report
  }

  // Final averages (update UI even if LLM fails)
  if (frameData.length > 0) {
    const avgPosture = frameData.reduce((sum, f) => sum + (100 - Math.abs(f.features?.shoulder_pitch || 0)), 0) / frameData.length;
    const avgQuality = frameData.reduce((sum, f) => sum + (f.features?.quality_score || 50), 0) / frameData.length;
    updateMetricUI('posture', avgPosture);
    updateMetricUI('balance', avgQuality);
    updateMetricUI('symmetry', avgQuality);
    updateMetricUI('motion', avgPosture);
  }

  // Show report in modal
  const reportSection = document.getElementById('report-section');
  if (reportSection) reportSection.style.display = 'block';
  showReportModal(report || 'Analysis complete, but report generation failed. Check console for data.');

  
}

  // Fallback local report generation (your original function, now used only on error)
  function generateReport() {
    if (frameData.length === 0) {
      return 'No analysis data available. Run an analysis first.';
    }

    const duration = document.getElementById('time-display')?.textContent || '5';
    const postureScore = document.getElementById('posture-score')?.textContent || 'N/A';
    const balanceScore = document.getElementById('balance-score')?.textContent || 'N/A';
    const symmetryScore = document.getElementById('symmetry-score')?.textContent || 'N/A';
    const motionScore = document.getElementById('motion-score')?.textContent || 'N/A';

    // Compute averages from collected data
    const avgFeatures = frameData.reduce((acc, frame) => {
      const f = frame.features || {};
      acc.pitch += Math.abs(f.shoulder_pitch || 0);
      acc.tilt += Math.abs(f.torso_tilt || 0);
      acc.quality += f.quality_score || 0;
      acc.velocity += f.joint_velocity || 0;
      acc.symmetry += f.step_symmetry || 0;
      return acc;
    }, { pitch: 0, tilt: 0, quality: 0, velocity: 0, symmetry: 0 });

    const numFrames = frameData.length;
    const avgPitch = Math.round(avgFeatures.pitch / numFrames);
    const avgTilt = Math.round(avgFeatures.tilt / numFrames);
    const avgQuality = Math.round(avgFeatures.quality / numFrames);
    const avgVelocity = Math.round(avgFeatures.velocity / numFrames * 10) / 10;
    const avgSymmetry = Math.round(avgFeatures.symmetry / numFrames * 100) / 100;

    const reportContent = `AI Critical Action Analyzer Report
================================================================================

📊 Analysis Summary
-------------------
- Duration: ${duration} seconds
- Total Frames Analyzed: ${numFrames} (sampled at ${SAMPLING_FPS} FPS)
- Timestamp: ${new Date().toISOString().slice(0, 19).replace('T', ' | ')}
- Device: ${navigator.userAgent.substring(0, 50)}...

🎯 Key Performance Metrics
--------------------------
Posture Score: ${postureScore} | Alignment Quality: ${100 - avgPitch}% (Ideal: >90%)
Balance Score: ${balanceScore} | Stability Deviation: Low (Target: >80%)
Symmetry Score: ${symmetryScore} | Limb Balance: ${avgSymmetry}% symmetry (Ideal: >85%)
Motion Quality: ${motionScore} | Avg Velocity: ${avgVelocity} px/s (Smooth: <5 variance)

📈 Pose & Movement Insights
---------------------------
- Average Shoulder Pitch Deviation: ${avgPitch}° (Recommendation: Keep <10° for optimal posture)
- Average Torso Tilt: ${avgTilt}° (Recommendation: Maintain <5° for balance)
- Landmark Visibility: ${avgQuality}% (Recommendation: Stay fully in frame for accuracy)
- Step/Movement Symmetry: ${avgSymmetry}% (Recommendation: Mirror left/right for efficiency)
- Overall Action Efficiency: ${Math.round((parseInt(postureScore) + parseInt(balanceScore) + parseInt(symmetryScore) + parseInt(motionScore)) / 4)}% 

💡 Personalized Recommendations
-------------------------------
${parseInt(postureScore) > 85 ? '✅ Excellent posture alignment! Continue maintaining straight torso.' : '⚠️ Improve posture: Align shoulders directly over hips to reduce strain.'}
${parseInt(balanceScore) > 80 ? '✅ Strong balance detected. Even weight distribution is effective.' : '⚠️ Enhance balance: Distribute weight evenly between feet to prevent sway.'}
${parseInt(symmetryScore) > 75 ? '✅ Good symmetry in movements. Low risk of overuse injuries.' : '⚠️ Focus on symmetry: Ensure left and right limbs move equally to avoid imbalances.'}
${parseInt(motionScore) > 80 ? '✅ Smooth, efficient motion. Great biomechanics!' : '⚠️ Refine motion: Slow down jerky movements for better control and reduced fatigue.'}

📝 Technical Notes
------------------
- Data collected via MediaPipe Pose (33 landmarks, visibility >${VISIBLE_THRESHOLD}).
- Sampling: ${SAMPLING_FPS} frames/second for ${duration}s.
- Full dataset logged in browser console (JSON format).
- For professional assessment, consult a certified trainer or physiotherapist.

Generated by AI Critical Action Analyzer | Stay Active & Balanced! 🚀
================================================================================`;

    return reportContent;
  }

  // Modal functions for displaying LLM/local report
  // Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Connect the generate report button
  const generateReportBtn = document.getElementById('generate-report-btn');
  if (generateReportBtn) {
    generateReportBtn.addEventListener('click', showStoredReport);
  }
  
  // Connect download button
  const downloadBtn = document.getElementById('download-report-btn');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadReport);
  }
  
  // Connect close button
  const closeBtn = document.getElementById('close-report-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeReportModal);
  }
});

// Store the latest report globally
let currentReport = '';

function showReportModal(reportContent) {
  const modal = document.getElementById('llm-report-modal');
  const contentEl = document.getElementById('llm-report-content');
  const closeBtn = document.querySelector('#llm-report-modal .close');

  if (!modal || !contentEl) {
    // Fallback: Alert if modal HTML missing
    alert(reportContent);
    return;
  }

  // Store the report
  currentReport = reportContent;
  
  // Format the report content with HTML
  contentEl.innerHTML = reportContent;
  modal.style.display = 'block';

  // Close handlers
  closeBtn.onclick = closeReportModal;
  modal.onclick = (e) => { 
    if (e.target === modal) closeReportModal(); 
  };
}

// Show stored report when button is clicked
function showStoredReport() {
  if (currentReport) {
    showReportModal(currentReport);
  } else {
    alert('No report available. Please complete an analysis first.');
  }
}

// Format the report content with beautiful HTML
function formatReportContent(reportText) {
  if (!reportText) return '<p>No report content available.</p>';
  
  // Convert markdown-like formatting to HTML
  let html = reportText
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/## (.*?)(?=\n|$)/g, '<h3>$1</h3>')
    .replace(/# (.*?)(?=\n|$)/g, '<h2>$1</h2>')
    .replace(/\n/g, '<br>')
    .replace(/- (.*?)(?=\n|$)/g, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/(\d+\/100)/g, '<div class="score">Overall Score: $1</div>')
    .replace(/(\d+%)/g, '<span class="percentage">$1</span>');
  
  return html;
}

function closeReportModal() {
  const modal = document.getElementById('llm-report-modal');
  if (modal) modal.style.display = 'none';
}

// Download report as text file
function downloadReport() {
  if (!currentReport) return;
  
  const blob = new Blob([currentReport], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `movement-analysis-report-${new Date().toISOString().split('T')[0]}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Global escape key for modal
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeReportModal();
  }
});

  // Start camera & analysis
  async function startCamera() {
    log('Starting analysis');
    if (isAnalyzing) return log('Already analyzing');

    video = document.querySelector('.input_video');
    canvas = document.querySelector('.output_canvas');
    if (!video || !canvas) {
      error('Missing video/canvas elements');
      alert('Required HTML elements missing. Check structure.');
      return;
    }

    ctx = canvas.getContext('2d');
    if (!ctx) {
      error('Canvas context failed');
      alert('Canvas setup error. Refresh page.');
      return;
    }

    const duration = parseInt(document.getElementById('time-display')?.textContent || '5');

    try {
      // Reset state
      frameData = [];
      previousLandmarks = null;
      latestLandmarks = [];
      noPoseTimer = 0;
      fpsCounter = { frames: 0, lastTime: 0 };
      window.lastVel = 0;

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        const overlayEl = document.getElementById('skeleton-overlay');
        const cameraOverlayEl = document.getElementById('camera-overlay');
        const startBtn = document.getElementById('start-camera');
        const stopBtn = document.getElementById('stop-camera');
        const captureBtn = document.getElementById('capture-frame');
        if (statusEl) statusEl.textContent = 'Initializing...';
        if (indicatorEl) indicatorEl.className = 'indicator-dot yellow';
        if (overlayEl) overlayEl.style.display = 'block';
        if (cameraOverlayEl) cameraOverlayEl.style.display = 'none';
        if (startBtn) startBtn.disabled = true;
        if (stopBtn) stopBtn.disabled = false;
        if (captureBtn) captureBtn.disabled = false;
      });

      // Wait for video ready
      await new Promise(resolve => {
        if (video.readyState >= 1) resolve();
        else {
          const onLoaded = () => {
            video.removeEventListener('loadedmetadata', onLoaded);
            resolve();
          };
          video.addEventListener('loadedmetadata', onLoaded);
          setTimeout(resolve, 100); // Fallback
        }
      });

      // Set canvas size (mobile optimized)
      const targetWidth = window.innerWidth < 768 ? 320 : 640;
      const targetHeight = window.innerWidth < 768 ? 240 : 480;
      canvas.width = targetWidth;
      canvas.height = targetHeight;
      canvas.style.width = `${targetWidth}px`;
      canvas.style.height = `${targetHeight}px`;

      // getUser Media (no space)
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Camera API not supported. Use modern browser.');
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: targetWidth },
          height: { ideal: targetHeight },
          facingMode: 'user' // Front camera
        }
      });
      video.srcObject = stream;

      // Camera init
      camera = new Camera(video, {
        onFrame: async () => {
          if (pose && isAnalyzing) {
            await pose.send({ image: video });
          }
        },
        width: targetWidth,
        height: targetHeight
      });
      await camera.start();

      log(`Camera active at ${targetWidth}x${targetHeight}`);

      // Skeleton (lazy init)
      if (!skeletonCanvas) initSkeleton();

      isAnalyzing = true;

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        if (statusEl) statusEl.textContent = 'Active';
        if (indicatorEl) indicatorEl.className = 'indicator-dot green';
      });

      // Start timer
      startAnalysisTimer(duration);

    } catch (err) {
      error('Start failed:', err);
      let msg = 'Analysis start failed. ';
      if (err.name === 'NotAllowedError') msg += 'Allow camera access.';
      else if (err.name === 'NotFoundError') msg += 'No camera found.';
      else msg += err.message || 'Unknown error.';
      alert(msg);

      batchUpdate(() => {
        const statusEl = document.getElementById('camera-status');
        const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
        const startBtn = document.getElementById('start-camera');
        if (statusEl) statusEl.textContent = 'Error';
        if (indicatorEl) indicatorEl.className = 'indicator-dot red';
        if (startBtn) startBtn.disabled = true;
      });
      isAnalyzing = false; // Fixed: was true before
    }
  }

    // Stop (manual or auto)
  function stopCamera() {
    log('Stopping analysis');
    // Cancel animation frame for immediate stop
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }

    // Camera stop (safe check)
    if (camera && typeof camera.stop === 'function') {
      camera.stop();
      camera = null;
    }

    if (sampleInterval) {
      clearInterval(sampleInterval);
      sampleInterval = null;
    }

    // Stop stream tracks
    if (video && video.srcObject) {
      video.srcObject.getTracks().forEach(track => track.stop());
      video.srcObject = null;
      video.pause();
    }
    
    isAnalyzing = false;

    batchUpdate(() => {
      const startBtn = document.getElementById('start-camera');
      const stopBtn = document.getElementById('stop-camera');
      const captureBtn = document.getElementById('capture-frame');
      const statusEl = document.getElementById('camera-status');
      const indicatorEl = document.querySelector('.camera-indicator .indicator-dot');
      const overlayEl = document.getElementById('skeleton-overlay');
      if (startBtn) startBtn.disabled = false;
      if (stopBtn) stopBtn.disabled = true;
      if (captureBtn) captureBtn.disabled = true;
      if (statusEl) statusEl.textContent = 'Stopped';
      if (indicatorEl) indicatorEl.className = 'indicator-dot red';
      if (overlayEl) overlayEl.style.display = 'block';

      // Clear skeleton
      if (skeletonCtx && skeletonCanvas) {
        skeletonCtx.clearRect(0, 0, skeletonCanvas.width, skeletonCanvas.height);
        drawStaticHuman2D();
      }
    });

    previousLandmarks = null;
    latestLandmarks = [];
    log('Analysis stopped');
  }

  // Reset (initial state)
  function resetData() {
    log('Resetting to initial state');
    stopCamera();
    frameData = [];

    if (ctx && canvas) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    // Skeleton reset
    if (skeletonCtx && skeletonCanvas) {
      skeletonCtx.clearRect(0, 0, skeletonCanvas.width, skeletonCanvas.height);
      drawStaticHuman2D();
    }

    batchUpdate(() => {
      const cameraOverlayEl = document.getElementById('camera-overlay');
      const statusEl = document.getElementById('camera-status');
      const skeletonIndicatorEl = document.querySelector('.skeleton-indicator .indicator-dot');

      if (cameraOverlayEl) cameraOverlayEl.style.display = 'block';
      if (statusEl) statusEl.textContent = 'Camera Off';
      if (skeletonIndicatorEl) skeletonIndicatorEl.className = 'indicator-dot red';

      // Reset metrics
      ['posture', 'balance', 'symmetry', 'motion'].forEach(type => {
        const scoreEl = document.getElementById(`${type}-score`);
        const progressEl = document.getElementById(`${type}-progress`);
        const trendEl = document.getElementById(`${type}-trend`);
        if (scoreEl) scoreEl.textContent = '0%';
        if (progressEl) progressEl.style.width = '0%';
        if (trendEl) trendEl.innerHTML = '<i class="fas fa-minus"></i> <span>No previous data</span>';
        localStorage.removeItem(`prev_${type}`);
      });
      
      const landmarksEl = document.getElementById('landmarks-count');
      const confEl = document.getElementById('confidence-score');
      const fpsEl = document.getElementById('frame-rate');
      const reportSection = document.getElementById('report-section');
      const progressEl = document.getElementById('analysis-progress');
      if (landmarksEl) landmarksEl.textContent = '0';
      if (confEl) confEl.textContent = '0%';
      if (fpsEl) fpsEl.textContent = '0 FPS';
      if (reportSection) reportSection.style.display = 'none';
      if (progressEl) progressEl.style.width = '0%';
    });

    fpsCounter = { frames: 0, lastTime: 0 };
    log('Reset complete');
  }

  // Capture frame (optional utility)
  function captureFrame() {
    if (!canvas || !isAnalyzing) {
      alert('No active frame. Start analysis first.');
      return;
    }

    const link = document.createElement('a');
    link.download = `pose-frame-${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    log('Frame captured');
  }

  // Timer slider (default 5s, user selectable)
  const timeSlider = document.getElementById('analysis-time-slider');
  const timeDisplay = document.getElementById('time-display');
  const selectedTimeValue = document.getElementById('selected-time-value');
  if (timeSlider && timeDisplay && selectedTimeValue) {
    timeSlider.min = 3;
    timeSlider.max = 30;
    timeSlider.value = 5; // Default
    timeDisplay.textContent = '5';
    selectedTimeValue.textContent = '5 seconds';
    timeSlider.addEventListener('input', (e) => {
      const value = parseInt(e.target.value);
      timeDisplay.textContent = value;
      selectedTimeValue.textContent = `${value} seconds`;
    });
  } else {
    // Fallback if elements missing
    if (timeDisplay) timeDisplay.textContent = '5';
  }

  // Event listeners (core buttons)
  const startBtn = document.getElementById('start-camera');
  if (startBtn) {
    startBtn.addEventListener('click', startCamera);
    log('Start button ready');
  }

  const stopBtn = document.getElementById('stop-camera');
  if (stopBtn) {
    stopBtn.addEventListener('click', stopCamera);
    log('Stop button ready');
  }

  const resetBtn = document.getElementById('reset-data');
  if (resetBtn) {
    resetBtn.addEventListener('click', resetData);
    log('Reset button ready');
  }

  const captureBtn = document.getElementById('capture-frame');
  if (captureBtn) {
    captureBtn.addEventListener('click', captureFrame);
    log('Capture button ready');
  }

  const reportBtn = document.getElementById('generate-report-btn');
  if (reportBtn) {
    reportBtn.addEventListener('click', () => {
      const localReport = generateReport();
      showReportModal(localReport);
    });
    log('Report button ready (fallback local)');
  }

  // Hero button (scroll + start)
  const heroBtn = document.getElementById('hero-analysis-btn');
  if (heroBtn) {
    heroBtn.addEventListener('click', () => {
      const analysisSection = document.getElementById('analysis');
      if (analysisSection) {
        analysisSection.scrollIntoView({ behavior: 'smooth' });
      }
      setTimeout(startCamera, 500); // Delay for smooth scroll
    });
    log('Hero button ready');
  }

  // Keyboard controls (Space: toggle start/stop, R: reset, G: generate local report)
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName.match(/^(INPUT|TEXTAREA|BUTTON)$/i) || e.target.isContentEditable) return;

    switch (e.key.toLowerCase()) {
      case ' ':
        e.preventDefault();
        if (isAnalyzing) {
          stopCamera();
        } else {
          startCamera();
        }
        startBtn?.focus(); // Accessibility
        break;
      case 'r':
        e.preventDefault();
        resetData();
        resetBtn?.focus();
        break;
      case 'g':
        e.preventDefault();
        const localReport = generateReport();
        showReportModal(localReport);
        break;
      case 'escape':
        if (isAnalyzing) stopCamera();
        else closeReportModal(); // Also closes modal
        break;
    }
  });

  // Cleanup on page unload (prevent memory leaks)
  window.addEventListener('beforeunload', () => {
    stopCamera();
    resetData();
    if (camera && typeof camera.stop === 'function') camera.stop();
    if (sampleInterval) clearInterval(sampleInterval);
    if (rafId) cancelAnimationFrame(rafId);
  });

  // Initial UI setup (reset to default state)
  batchUpdate(() => {
    const cameraOverlayEl = document.getElementById('camera-overlay');
    const statusEl = document.getElementById('camera-status');
    const indicators = document.querySelectorAll('.indicator-dot');
    const stats = document.querySelectorAll('.stat-value, .progress-fill');
    const trends = document.querySelectorAll('[id$="-trend"]');
    const reportSection = document.getElementById('report-section');
    const progressEl = document.getElementById('analysis-progress');

    if (cameraOverlayEl) cameraOverlayEl.style.display = 'block';
    if (statusEl) statusEl.textContent = 'Camera Off';

    indicators.forEach(el => el.className = 'indicator-dot red');
    stats.forEach(el => {
      if (el.classList.contains('stat-value')) el.textContent = '0%';
      else if (el.classList.contains('progress-fill')) el.style.width = '0%';
    });
    trends.forEach(el => el.innerHTML = '<i class="fas fa-minus"></i> <span>No previous data</span>');

    if (reportSection) reportSection.style.display = 'none';
    if (progressEl) progressEl.style.width = '0%';

    // Clear trends in localStorage
    ['posture', 'balance', 'symmetry', 'motion'].forEach(type => localStorage.removeItem(`prev_${type}`));
  });

  // Pre-initialize (non-blocking)
  initSkeleton(); // Setup skeleton (2D fallback if WebGL fails)
  log('AI Critical Action Analyzer fully initialized');
  log('Ready for analysis. Select timer, click Start, and perform actions in frame.');
});
            
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
