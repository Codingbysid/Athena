"""
🎨 Premium Athena UI Styles - Dark Theme with 3D Animations
Sophisticated design system inspired by Mont-Fort with high-performance animations
"""

import streamlit as st

def load_advanced_css():
    """Load premium dark theme CSS with 3D animations and tactile interactions"""
    
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Premium Dark Theme Design System */
    :root {
        /* Dark Theme Colors */
        --bg-primary: #0a0a0a;
        --bg-secondary: #111111;
        --bg-tertiary: #1a1a1a;
        --bg-card: #1e1e1e;
        --bg-overlay: rgba(0, 0, 0, 0.8);
        
        /* Accent Colors */
        --primary: #667eea;
        --primary-light: #7c8fff;
        --primary-dark: #4c63d2;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
        
        /* Gradients */
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        --danger-gradient: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        --dark-gradient: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        
        /* Text Colors */
        --text-primary: #ffffff;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        --text-accent: #667eea;
        
        /* Shadows & Depth */
        --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 8px 16px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 16px 32px rgba(0, 0, 0, 0.5);
        --shadow-xl: 0 24px 48px rgba(0, 0, 0, 0.6);
        --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.3);
        
        /* Spacing */
        --space-xs: 0.25rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
        --space-2xl: 3rem;
        --space-3xl: 4rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        
        /* Transitions */
        --transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        
        /* 3D Transforms */
        --perspective: 1000px;
        --depth-sm: translateZ(10px);
        --depth-md: translateZ(20px);
        --depth-lg: translateZ(30px);
    }
    
    /* Reset & Base Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Dark Theme Base */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
    }
    
    /* Main App Container */
    .main .block-container {
        padding: var(--space-xl);
        max-width: 1400px;
        margin: 0 auto;
        background: transparent;
    }
    
    /* Premium Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.025em;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--space-lg);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.3)); }
        to { filter: drop-shadow(0 0 30px rgba(102, 126, 234, 0.6)); }
    }
    
    .sub-header {
        font-size: 1.25rem;
        font-weight: 500;
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: var(--space-xl);
        animation: fadeInUp 1s ease-out 0.3s both;
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
    
    /* 3D Card Components */
    .metric-card-3d {
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        padding: var(--space-xl);
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition-normal);
        transform-style: preserve-3d;
        perspective: var(--perspective);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-3d::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--primary-gradient);
        opacity: 0;
        transition: var(--transition-normal);
        z-index: -1;
    }
    
    .metric-card-3d:hover {
        transform: translateY(-8px) var(--depth-md);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
        border-color: var(--primary);
    }
    
    .metric-card-3d:hover::before {
        opacity: 0.1;
    }
    
    .metric-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: var(--space-sm);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: var(--space-xs);
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--success);
        display: flex;
        align-items: center;
        gap: var(--space-xs);
    }
    
    .metric-change.negative {
        color: var(--danger);
    }
    
    /* 3D Feature Cards */
    .feature-card-3d {
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        padding: var(--space-2xl);
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition-normal);
        transform-style: preserve-3d;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card-3d::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: var(--transition-slow);
    }
    
    .feature-card-3d:hover {
        transform: translateY(-8px) var(--depth-md);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .feature-card-3d:hover::after {
        left: 100%;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: var(--space-lg);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: var(--space-md);
    }
    
    .feature-description {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: var(--text-primary);
        border: none;
        border-radius: var(--radius-lg);
        padding: var(--space-md) var(--space-xl);
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition-normal);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: var(--transition-slow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) var(--depth-sm);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* 3D Form Elements */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input {
        background: var(--bg-tertiary);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: var(--radius-md);
        color: var(--text-primary);
        padding: var(--space-md);
        transition: var(--transition-fast);
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: var(--shadow-md), 0 0 0 3px rgba(102, 126, 234, 0.1);
        transform: var(--depth-sm);
    }
    
    /* Premium Messages */
    .success-message-3d {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid var(--success);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        color: var(--success);
        margin: var(--space-md) 0;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.5s ease-out;
    }
    
    .error-message-3d {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 1px solid var(--danger);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        color: var(--danger);
        margin: var(--space-md) 0;
        box-shadow: var(--shadow-md);
        animation: shake 0.5s ease-out;
    }
    
    .info-message-3d {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%);
        border: 1px solid var(--info);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        color: var(--info);
        margin: var(--space-md) 0;
        box-shadow: var(--shadow-md);
        animation: fadeIn 0.5s ease-out;
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
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* 3D Loading Animation */
    .loading-3d {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: var(--space-2xl);
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
        border-radius: var(--radius-sm);
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
    
    /* Floating Particles Background */
    .particles-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: var(--primary);
        border-radius: 50%;
        opacity: 0.6;
        animation: floatParticle 8s infinite ease-in-out;
    }
    
    @keyframes floatParticle {
        0%, 100% {
            transform: translateY(0px) translateX(0px);
            opacity: 0.6;
        }
        50% {
            transform: translateY(-100px) translateX(50px);
            opacity: 0.2;
        }
    }
    
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; }
    .particle:nth-child(2) { left: 20%; animation-delay: 1s; }
    .particle:nth-child(3) { left: 30%; animation-delay: 2s; }
    .particle:nth-child(4) { left: 40%; animation-delay: 3s; }
    .particle:nth-child(5) { left: 50%; animation-delay: 4s; }
    .particle:nth-child(6) { left: 60%; animation-delay: 5s; }
    .particle:nth-child(7) { left: 70%; animation-delay: 6s; }
    .particle:nth-child(8) { left: 80%; animation-delay: 7s; }
    .particle:nth-child(9) { left: 90%; animation-delay: 8s; }
    .particle:nth-child(10) { left: 95%; animation-delay: 9s; }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--space-md);
        }
        
        .main-header {
            font-size: 2.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .feature-card-3d {
            padding: var(--space-lg);
        }
    }
    
    /* Accessibility */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* High Contrast Mode */
    @media (prefers-contrast: high) {
        .metric-card-3d, .feature-card-3d {
            border: 2px solid var(--text-primary);
        }
        
        .stButton > button {
            border: 2px solid var(--text-primary);
        }
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_metric_card_3d(title: str, value: str, change: str = None, change_type: str = "positive"):
    """Create a premium 3D metric card"""
    change_class = "" if not change else f" {change_type}"
    change_html = f'<div class="metric-change{change_class}">{change}</div>' if change else ""
    
    return f"""
    <div class="metric-card-3d">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """

def create_feature_card_3d(title: str, description: str, icon: str = "🚀"):
    """Create a premium 3D feature card"""
    return f"""
    <div class="feature-card-3d">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-description">{description}</div>
    </div>
    """

def create_success_message_3d(message: str):
    """Create a premium success message"""
    return f'<div class="success-message-3d">✅ {message}</div>'

def create_error_message_3d(message: str):
    """Create a premium error message"""
    return f'<div class="error-message-3d">❌ {message}</div>'

def create_info_message_3d(message: str):
    """Create a premium info message"""
    return f'<div class="info-message-3d">ℹ️ {message}</div>'

def create_loading_3d():
    """Create a premium 3D loading animation"""
    return """
    <div class="loading-3d">
        <div class="loading-cube">
            <div class="cube-face front"></div>
            <div class="cube-face back"></div>
            <div class="cube-face right"></div>
            <div class="cube-face left"></div>
            <div class="cube-face top"></div>
            <div class="cube-face bottom"></div>
        </div>
    </div>
    """

def add_floating_particles():
    """Add floating particles background"""
    particles_html = """
    <div class="particles-container">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """
    return particles_html