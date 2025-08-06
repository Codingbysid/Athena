"""
🎨 Advanced Athena UI Styles & Animations
Professional styling for hackathon-winning presentation
"""

import streamlit as st

def load_advanced_css():
    """Load advanced CSS with animations and professional styling"""
    
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Global Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --danger-gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        --dark-gradient: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        --light-bg: rgba(255, 255, 255, 0.95);
        --shadow-light: 0 4px 20px rgba(0, 0, 0, 0.1);
        --shadow-medium: 0 8px 30px rgba(0, 0, 0, 0.15);
        --shadow-heavy: 0 12px 40px rgba(0, 0, 0, 0.2);
        --border-radius: 15px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Main App Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom Font Family */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #667eea, #764ba2);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main Content Area */
    .main {
        background: var(--light-bg);
        backdrop-filter: blur(20px);
        border-radius: var(--border-radius);
        margin: 1rem;
        box-shadow: var(--shadow-heavy);
        animation: slideUp 0.8s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header Animations */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        animation: titleGlow 2s ease-in-out infinite alternate;
        letter-spacing: -0.02em;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 10px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.6)); }
    }
    
    .sub-header {
        font-size: 1.4rem;
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out 0.3s both;
        font-weight: 400;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced Cards */
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-medium);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: var(--primary-gradient);
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin: 1rem;
        box-shadow: var(--shadow-medium);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(-45deg);
        transition: var(--transition);
        opacity: 0;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-heavy);
    }
    
    .metric-card:hover::before {
        animation: shimmer 1s ease;
        opacity: 1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(-45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(-45deg); }
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition);
        box-shadow: var(--shadow-light);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:focus {
        outline: none;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
    }
    
    /* Form Enhancements */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: var(--transition);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: var(--transition);
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: var(--transition);
        animation: fadeInScale 0.6s ease-out;
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .chart-container:hover {
        box-shadow: var(--shadow-medium);
    }
    
    /* Insight Panels */
    .insight-panel {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: var(--shadow-light);
        transition: var(--transition);
        position: relative;
    }
    
    .insight-panel::before {
        content: '💡';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 1.5rem;
        opacity: 0.3;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    .insight-panel:hover {
        transform: translateX(5px);
        border-left-width: 8px;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background: var(--primary-gradient);
        border-radius: 10px;
        height: 12px;
        animation: progressFill 1.5s ease-out;
    }
    
    @keyframes progressFill {
        from { width: 0; }
        to { width: var(--progress-width, 100%); }
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: var(--primary-gradient);
        color: white;
    }
    
    .css-1d391kg .css-17eq0hr {
        color: white;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-color: #667eea transparent #667eea transparent;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: var(--success-gradient);
        border: none;
        border-radius: var(--border-radius);
        animation: slideInRight 0.5s ease-out;
    }
    
    .stError {
        background: var(--danger-gradient);
        border: none;
        border-radius: var(--border-radius);
        animation: shake 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Metric Value Animations */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from { 
            opacity: 0;
            transform: scale(0.5);
        }
        to { 
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Floating Elements */
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .metric-card {
            margin: 0.5rem;
            padding: 1.5rem;
        }
        
        .feature-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a67d8;
    }
    
    /* 3D Hero Section */
    .hero-3d-container {
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        background: var(--primary-gradient);
    }
    
    .floating-cube {
        position: absolute;
        width: 100px;
        height: 100px;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        animation: float 6s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .cube-1 {
        top: 20%;
        left: 10%;
        animation-delay: 0s;
        transform: rotateX(45deg) rotateY(45deg);
    }
    
    .cube-2 {
        top: 60%;
        right: 15%;
        animation-delay: 2s;
        transform: rotateX(-30deg) rotateY(60deg);
    }
    
    .cube-3 {
        bottom: 20%;
        left: 50%;
        animation-delay: 4s;
        transform: rotateX(60deg) rotateY(-45deg);
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px) rotateX(45deg) rotateY(45deg);
        }
        50% {
            transform: translateY(-20px) rotateX(45deg) rotateY(45deg);
        }
    }
    
    .hero-content {
        text-align: center;
        color: white;
        z-index: 10;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .hero-description {
        font-size: 1.2rem;
        opacity: 0.8;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* 3D Metric Cards */
    .metric-card-3d {
        perspective: 1000px;
        margin: 20px 0;
    }
    
    .metric-card-inner {
        background: var(--primary-gradient);
        border-radius: 20px;
        padding: 30px;
        color: white;
        text-align: center;
        box-shadow: var(--shadow-heavy);
        transition: all 0.5s ease;
        transform-style: preserve-3d;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-inner:hover {
        transform: translateY(-10px) rotateX(5deg) rotateY(5deg);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .metric-title {
        font-size: 1.2rem;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .metric-change {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .metric-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    
    .metric-card-inner:hover .metric-glow {
        transform: translateX(100%);
    }
    
    /* 3D Feature Cards */
    .feature-card-3d {
        perspective: 1000px;
        margin: 20px 0;
    }
    
    .feature-card-inner {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: var(--shadow-medium);
        transition: all 0.5s ease;
        transform-style: preserve-3d;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-card-inner:hover {
        transform: translateY(-10px) rotateX(5deg) rotateY(5deg);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        text-align: center;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .feature-title {
        color: #1e293b;
        margin-bottom: 15px;
        font-size: 1.4rem;
        font-weight: bold;
    }
    
    .feature-description {
        color: #64748b;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .feature-glow {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.5s ease;
    }
    
    .feature-card-inner:hover .feature-glow {
        transform: translateX(100%);
    }
    
    /* 3D Parallax Section */
    .parallax-section {
        position: relative;
        height: 400px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--primary-gradient);
    }
    
    .parallax-layer {
        position: absolute;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: parallax 10s ease-in-out infinite;
    }
    
    .layer-1 {
        animation-delay: 0s;
        transform: scale(0.5);
    }
    
    .layer-2 {
        animation-delay: 2s;
        transform: scale(0.8);
    }
    
    .layer-3 {
        animation-delay: 4s;
        transform: scale(1.2);
    }
    
    @keyframes parallax {
        0%, 100% {
            transform: translateY(0px) scale(1);
        }
        50% {
            transform: translateY(-50px) scale(1.1);
        }
    }
    
    .parallax-content {
        text-align: center;
        color: white;
        z-index: 10;
    }
    
    .parallax-content h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .parallax-content p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Floating Elements */
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-element {
        position: absolute;
        width: 50px;
        height: 50px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 50%;
        animation: floatElement 8s ease-in-out infinite;
    }
    
    .element-1 {
        top: 10%;
        left: 10%;
        animation-delay: 0s;
    }
    
    .element-2 {
        top: 20%;
        right: 15%;
        animation-delay: 2s;
    }
    
    .element-3 {
        bottom: 30%;
        left: 20%;
        animation-delay: 4s;
    }
    
    .element-4 {
        top: 60%;
        right: 10%;
        animation-delay: 6s;
    }
    
    .element-5 {
        bottom: 20%;
        right: 30%;
        animation-delay: 8s;
    }
    
    @keyframes floatElement {
        0%, 100% {
            transform: translateY(0px) rotate(0deg);
        }
        50% {
            transform: translateY(-30px) rotate(180deg);
        }
    }
    
    /* 3D Navigation */
    .nav-3d {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }
    
    .nav-item {
        perspective: 1000px;
        cursor: pointer;
    }
    
    .nav-item > div {
        background: var(--primary-gradient);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        transform-style: preserve-3d;
    }
    
    .nav-item:hover > div {
        transform: translateY(-5px) rotateX(10deg) rotateY(10deg);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .nav-icon {
        font-size: 2rem;
        display: block;
        margin-bottom: 10px;
    }
    
    .nav-text {
        font-weight: 600;
    }
    
    /* 3D Loading Animation */
    .loading-3d {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .loading-cube {
        width: 60px;
        height: 60px;
        position: relative;
        transform-style: preserve-3d;
        animation: rotate 2s infinite linear;
    }
    
    .cube-face {
        position: absolute;
        width: 60px;
        height: 60px;
        background: var(--primary-gradient);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }
    
    .front { transform: translateZ(30px); }
    .back { transform: translateZ(-30px); }
    .right { transform: rotateY(90deg) translateZ(30px); }
    .left { transform: rotateY(-90deg) translateZ(30px); }
    .top { transform: rotateX(90deg) translateZ(30px); }
    .bottom { transform: rotateX(-90deg) translateZ(30px); }
    
    @keyframes rotate {
        0% { transform: rotateX(0deg) rotateY(0deg); }
        100% { transform: rotateX(360deg) rotateY(360deg); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    /* Risk Level Colors */
    .risk-low { 
        background: var(--success-gradient);
        animation: glow-green 2s ease-in-out infinite alternate;
    }
    
    .risk-medium { 
        background: var(--warning-gradient);
        animation: glow-orange 2s ease-in-out infinite alternate;
    }
    
    .risk-high { 
        background: var(--danger-gradient);
        animation: glow-red 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow-green {
        from { box-shadow: 0 0 20px rgba(79, 172, 254, 0.3); }
        to { box-shadow: 0 0 30px rgba(79, 172, 254, 0.6); }
    }
    
    @keyframes glow-orange {
        from { box-shadow: 0 0 20px rgba(250, 112, 154, 0.3); }
        to { box-shadow: 0 0 30px rgba(250, 112, 154, 0.6); }
    }
    
    @keyframes glow-red {
        from { box-shadow: 0 0 20px rgba(255, 107, 107, 0.3); }
        to { box-shadow: 0 0 30px rgba(255, 107, 107, 0.6); }
    }
    
    /* Typewriter Effect */
    .typewriter {
        overflow: hidden;
        border-right: .15em solid orange;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: orange; }
    }
    
    /* Data Table Enhancements */
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-light);
        animation: slideInUp 0.6s ease-out;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Loading Skeleton */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Enhanced Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_animated_metric(label, value, delta=None, help_text=None):
    """Create an animated metric display"""
    
    delta_html = ""
    if delta:
        delta_color = "green" if delta > 0 else "red"
        delta_symbol = "+" if delta > 0 else ""
        delta_html = f'<small style="color: {delta_color};">{delta_symbol}{delta}</small>'
    
    metric_html = f"""
    <div class="metric-card floating">
        <div class="metric-value">{value}</div>
        <p style="margin: 0.5rem 0 0 0; font-weight: 500;">{label}</p>
        {delta_html}
    </div>
    """
    
    return metric_html

def create_typing_text(text, speed=50):
    """Create typewriter effect for text"""
    return f'<div class="typewriter" style="animation-duration: {len(text)/speed}s;">{text}</div>'

def create_loading_placeholder():
    """Create a loading skeleton placeholder"""
    return """
    <div class="skeleton" style="height: 200px; border-radius: 15px; margin: 1rem 0;"></div>
    """

def add_particles_background():
    """Add animated particles background"""
    particles_js = """
    <div id="particles-js" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    particlesJS('particles-js', {
        particles: {
            number: { value: 80, density: { enable: true, value_area: 800 } },
            color: { value: "#667eea" },
            shape: { type: "circle", stroke: { width: 0, color: "#000000" } },
            opacity: { value: 0.5, random: false },
            size: { value: 3, random: true },
            line_linked: { enable: true, distance: 150, color: "#667eea", opacity: 0.4, width: 1 },
            move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
        },
        interactivity: {
            detect_on: "canvas",
            events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
            modes: { grab: { distance: 400, line_linked: { opacity: 1 } }, bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 }, repulse: { distance: 200, duration: 0.4 }, push: { particles_nb: 4 }, remove: { particles_nb: 2 } }
        },
        retina_detect: true
    });
    </script>
    """
    return particles_js