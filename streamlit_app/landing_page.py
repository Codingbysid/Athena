"""
🌟 Athena Landing Page - Premium Authentication & User Experience
Beautiful landing page with sophisticated authentication flow
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import hashlib
import secrets

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent / "utils"))
sys.path.append(str(Path(__file__).parent / "components"))
sys.path.append(str(Path(__file__).parent / "styles"))

# Import our custom modules
from athena_styles import (
    load_advanced_css, create_metric_card_3d, create_feature_card_3d,
    create_success_message_3d, create_error_message_3d, create_info_message_3d,
    add_floating_particles
)

# Load premium CSS with 3D animations
load_advanced_css()

# Page configuration
st.set_page_config(
    page_title="Athena - AI Sales Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_landing_css():
    """Load additional CSS for the landing page"""
    css = """
    <style>
    /* Landing Page Specific Styles */
    .hero-section {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        position: relative;
        overflow: hidden;
    }
    
    .hero-content {
        text-align: center;
        z-index: 10;
        position: relative;
        max-width: 800px;
        padding: 2rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        animation: fadeInUp 1s ease-out 0.5s both;
        line-height: 1.4;
    }
    
    .hero-description {
        font-size: 1.2rem;
        color: var(--text-muted);
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out 0.7s both;
        line-height: 1.6;
    }
    
    .cta-buttons {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out 0.9s both;
        flex-wrap: wrap;
    }
    
    .cta-primary {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: var(--radius-lg);
        font-weight: 600;
        font-size: 1.2rem;
        cursor: pointer;
        transition: var(--transition-normal);
        box-shadow: var(--shadow-md);
        text-decoration: none;
        display: inline-block;
        position: relative;
        overflow: hidden;
    }
    
    .cta-primary::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: var(--transition-slow);
    }
    
    .cta-primary:hover::before {
        left: 100%;
    }
    
    .cta-primary:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
    }
    
    .cta-secondary {
        background: transparent;
        color: var(--primary);
        border: 2px solid var(--primary);
        padding: 1.2rem 2.5rem;
        border-radius: var(--radius-lg);
        font-weight: 600;
        font-size: 1.2rem;
        cursor: pointer;
        transition: var(--transition-normal);
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-secondary:hover {
        background: var(--primary);
        color: white;
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
    }
    
    /* Features Section */
    .features-section {
        padding: 6rem 0;
        background: var(--bg-secondary);
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2.5rem;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .feature-card {
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition-normal);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: var(--transition-slow);
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: var(--text-secondary);
        line-height: 1.7;
        font-size: 1.1rem;
    }
    
    /* Stats Section */
    .stats-section {
        padding: 6rem 0;
        background: var(--bg-primary);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 3rem;
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .stat-card {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition-normal);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 900;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: var(--text-secondary);
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Demo Section */
    .demo-section {
        padding: 6rem 0;
        background: var(--bg-secondary);
        text-align: center;
    }
    
    .demo-content {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .demo-title {
        font-size: 3rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 1.5rem;
    }
    
    .demo-description {
        font-size: 1.3rem;
        color: var(--text-secondary);
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    
    .demo-buttons {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .demo-button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1.2rem 2.5rem;
        border-radius: var(--radius-lg);
        font-weight: 600;
        font-size: 1.2rem;
        cursor: pointer;
        transition: var(--transition-normal);
        box-shadow: var(--shadow-md);
        text-decoration: none;
        display: inline-block;
    }
    
    .demo-button:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 3rem;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
        }
        
        .hero-description {
            font-size: 1rem;
        }
        
        .cta-buttons {
            flex-direction: column;
            align-items: center;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .demo-title {
            font-size: 2.5rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_hero_section():
    """Create the hero section"""
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">🚀 ATHENA</h1>
            <p class="hero-subtitle">AI-Powered Sales Intelligence Platform</p>
            <p class="hero-description">
                Transform your sales pipeline with intelligent health scoring, predictive analytics, 
                and AI-powered insights. Boost win rates by 15% and reduce sales cycles by 20%.
            </p>
            <div class="cta-buttons">
                <a href="#" class="cta-primary" onclick="window.location.href='auth_system.py'">Get Started</a>
                <a href="#" class="cta-secondary" onclick="window.location.href='🏠_Home.py'">Try Demo</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_features_section():
    """Create the features section"""
    st.markdown("""
    <div class="features-section">
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI-Powered Insights</h3>
                <p class="feature-description">
                    Advanced machine learning models provide real-time health scoring and predictive analytics 
                    for your sales opportunities with 70% accuracy.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Portfolio Analytics</h3>
                <p class="feature-description">
                    Comprehensive dashboards and visualizations to monitor your entire sales pipeline 
                    health and performance in real-time.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 class="feature-title">Automated Workflows</h3>
                <p class="feature-description">
                    Seamless integration with Salesforce and Slack for automated alerts and 
                    rescue strategies for at-risk opportunities.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_stats_section():
    """Create the stats section"""
    st.markdown("""
    <div class="stats-section">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">70%</div>
                <div class="stat-label">Model Accuracy</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">15%</div>
                <div class="stat-label">Win Rate Increase</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">20%</div>
                <div class="stat-label">Sales Cycle Reduction</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">85%</div>
                <div class="stat-label">Forecast Accuracy</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_demo_section():
    """Create the demo section"""
    st.markdown("""
    <div class="demo-section">
        <div class="demo-content">
            <h2 class="demo-title">Ready to Experience Athena?</h2>
            <p class="demo-description">
                See how AI-powered sales intelligence can transform your pipeline. 
                Try our interactive demo or create an account to get started.
            </p>
            <div class="demo-buttons">
                <a href="#" class="demo-button" onclick="window.location.href='auth_system.py'">Create Account</a>
                <a href="#" class="demo-button" onclick="window.location.href='🏠_Home.py'">Try Demo</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Load landing page CSS
    load_landing_css()
    
    # Check if user is authenticated
    if st.session_state.get('authenticated', False):
        # Redirect to main app
        st.switch_page("🏠_Home.py")
    else:
        # Show landing page
        create_hero_section()
        create_features_section()
        create_stats_section()
        create_demo_section()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
            <p style="font-size: 1.1rem;">Built with ❤️ for the hackathon | Powered by AI & ML</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 