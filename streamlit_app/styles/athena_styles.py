"""
🎨 Clean & Professional Athena UI Styles
Optimized for hackathon presentation and user experience
"""

import streamlit as st

def load_advanced_css():
    """Load clean, professional CSS with subtle animations"""
    
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Design System Variables */
    :root {
        /* Colors */
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --secondary: #64748b;
        --success: #059669;
        --warning: #d97706;
        --danger: #dc2626;
        --info: #0891b2;
        
        /* Gradients */
        --primary-gradient: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        --success-gradient: linear-gradient(135deg, #059669 0%, #047857 100%);
        --warning-gradient: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        --danger-gradient: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        
        /* Backgrounds */
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --bg-dark: #0f172a;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
        
        /* Spacing */
        --space-xs: 0.25rem;
        --space-sm: 0.5rem;
        --space-md: 1rem;
        --space-lg: 1.5rem;
        --space-xl: 2rem;
        --space-2xl: 3rem;
        
        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        
        /* Transitions */
        --transition-fast: 0.15s ease;
        --transition-normal: 0.3s ease;
        --transition-slow: 0.5s ease;
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
    
    /* Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
        color: #1e293b;
    }
    
    /* Main App Container */
    .main .block-container {
        padding: var(--space-xl);
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Clean Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: var(--primary);
        margin-bottom: var(--space-lg);
        letter-spacing: -0.025em;
    }
    
    .sub-header {
        font-size: 1.25rem;
        font-weight: 500;
        text-align: center;
        color: var(--secondary);
        margin-bottom: var(--space-xl);
    }
    
    /* Card Components */
    .metric-card {
        background: var(--bg-primary);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-md);
        border: 1px solid #e2e8f0;
        transition: var(--transition-normal);
        margin-bottom: var(--space-md);
    }
    
    .metric-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .metric-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--secondary);
        margin-bottom: var(--space-sm);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: var(--space-xs);
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--success);
    }
    
    .metric-change.negative {
        color: var(--danger);
    }
    
    /* Feature Cards */
    .feature-card {
        background: var(--bg-primary);
        border-radius: var(--radius-lg);
        padding: var(--space-xl);
        box-shadow: var(--shadow-md);
        border: 1px solid #e2e8f0;
        transition: var(--transition-normal);
        height: 100%;
    }
    
    .feature-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: var(--space-md);
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: var(--space-sm);
    }
    
    .feature-description {
        color: var(--secondary);
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--space-md) var(--space-xl);
        font-weight: 600;
        transition: var(--transition-normal);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Form Elements */
    .stTextInput > div > div > input {
        border-radius: var(--radius-md);
        border: 1px solid #d1d5db;
        padding: var(--space-md);
        transition: var(--transition-fast);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
    }
    
    .stSelectbox > div > div > div {
        border-radius: var(--radius-md);
        border: 1px solid #d1d5db;
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border: 1px solid #10b981;
        border-radius: var(--radius-md);
        padding: var(--space-md);
        color: #065f46;
        margin: var(--space-md) 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 1px solid #ef4444;
        border-radius: var(--radius-md);
        padding: var(--space-md);
        color: #991b1b;
        margin: var(--space-md) 0;
    }
    
    .info-message {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #3b82f6;
        border-radius: var(--radius-md);
        padding: var(--space-md);
        color: #1e40af;
        margin: var(--space-md) 0;
    }
    
    /* Loading States */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: var(--space-xl);
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid #e2e8f0;
        border-top: 3px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--space-md);
        }
        
        .main-header {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .feature-card {
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
        .metric-card, .feature-card {
            border: 2px solid #000;
        }
        
        .stButton > button {
            border: 2px solid #000;
        }
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, change: str = None, change_type: str = "positive"):
    """Create a clean metric card"""
    change_class = "" if not change else f" {change_type}"
    change_html = f'<div class="metric-change{change_class}">{change}</div>' if change else ""
    
    return f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {change_html}
    </div>
    """

def create_feature_card(title: str, description: str, icon: str = "🚀"):
    """Create a clean feature card"""
    return f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-description">{description}</div>
    </div>
    """

def create_success_message(message: str):
    """Create a success message"""
    return f'<div class="success-message">✅ {message}</div>'

def create_error_message(message: str):
    """Create an error message"""
    return f'<div class="error-message">❌ {message}</div>'

def create_info_message(message: str):
    """Create an info message"""
    return f'<div class="info-message">ℹ️ {message}</div>'

def create_loading_spinner():
    """Create a loading spinner"""
    return """
    <div class="loading-container">
        <div class="loading-spinner"></div>
    </div>
    """