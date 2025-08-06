"""
🔐 Athena Authentication System
Premium authentication with Supabase integration and beautiful UI
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import hashlib
import secrets
import json
from datetime import datetime, timedelta

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

def load_auth_css():
    """Load additional CSS for authentication"""
    css = """
    <style>
    /* Authentication Specific Styles */
    .auth-page {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%);
        position: relative;
        overflow: hidden;
    }
    
    .auth-container {
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        padding: 3rem;
        max-width: 450px;
        width: 90%;
        box-shadow: var(--shadow-xl);
        border: 1px solid rgba(255, 255, 255, 0.1);
        animation: authSlideIn 0.5s ease-out;
        position: relative;
        z-index: 10;
    }
    
    @keyframes authSlideIn {
        from {
            opacity: 0;
            transform: translateY(-30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-logo {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    
    .auth-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .auth-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .form-group {
        position: relative;
    }
    
    .form-label {
        display: block;
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .form-input {
        width: 100%;
        background: var(--bg-tertiary);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        padding: 1rem;
        color: var(--text-primary);
        font-size: 1rem;
        transition: var(--transition-fast);
        box-sizing: border-box;
    }
    
    .form-input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    .form-input.error {
        border-color: var(--danger);
    }
    
    .form-input.success {
        border-color: var(--success);
    }
    
    .password-toggle {
        position: absolute;
        right: 1rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        font-size: 1.2rem;
    }
    
    .auth-button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem;
        border-radius: var(--radius-md);
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: var(--transition-normal);
        margin-top: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .auth-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: var(--transition-slow);
    }
    
    .auth-button:hover::before {
        left: 100%;
    }
    
    .auth-button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg), var(--shadow-glow);
    }
    
    .auth-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    .auth-divider {
        text-align: center;
        margin: 2rem 0;
        position: relative;
        color: var(--text-secondary);
    }
    
    .auth-divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .auth-divider span {
        background: var(--bg-card);
        padding: 0 1rem;
        position: relative;
        z-index: 1;
    }
    
    .social-auth {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .social-button {
        flex: 1;
        background: var(--bg-tertiary);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        padding: 1rem;
        color: var(--text-primary);
        font-weight: 600;
        cursor: pointer;
        transition: var(--transition-fast);
        text-align: center;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .social-button:hover {
        background: var(--bg-secondary);
        border-color: var(--primary);
        transform: translateY(-1px);
    }
    
    .auth-switch {
        text-align: center;
        margin-top: 2rem;
        color: var(--text-secondary);
    }
    
    .auth-switch a {
        color: var(--primary);
        text-decoration: none;
        font-weight: 600;
        transition: var(--transition-fast);
    }
    
    .auth-switch a:hover {
        text-decoration: underline;
    }
    
    .error-message {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border: 1px solid var(--danger);
        border-radius: var(--radius-md);
        padding: 1rem;
        color: var(--danger);
        margin-bottom: 1rem;
        animation: shake 0.5s ease-out;
    }
    
    .success-message {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
        border: 1px solid var(--success);
        border-radius: var(--radius-md);
        padding: 1rem;
        color: var(--success);
        margin-bottom: 1rem;
        animation: slideInRight 0.5s ease-out;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .auth-container {
            padding: 2rem;
            margin: 1rem;
        }
        
        .auth-title {
            font-size: 2rem;
        }
        
        .social-auth {
            flex-direction: column;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_login_page():
    """Create the login page"""
    st.markdown("""
    <div class="auth-page">
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-logo">🚀</div>
                <h1 class="auth-title">Welcome Back</h1>
                <p class="auth-subtitle">Sign in to your Athena account</p>
            </div>
            
            <form class="auth-form">
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-input" placeholder="Enter your email" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-input" placeholder="Enter your password" required>
                    <button type="button" class="password-toggle">👁️</button>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <label style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary);">
                        <input type="checkbox" style="margin: 0;">
                        Remember me
                    </label>
                    <a href="#" style="color: var(--primary); text-decoration: none; font-size: 0.9rem;">Forgot password?</a>
                </div>
                
                <button type="submit" class="auth-button">
                    <span class="loading-spinner" style="display: none;"></span>
                    Sign In
                </button>
            </form>
            
            <div class="auth-divider">
                <span>or continue with</span>
            </div>
            
            <div class="social-auth">
                <a href="#" class="social-button">
                    <span>🔍</span>
                    Google
                </a>
                <a href="#" class="social-button">
                    <span>💼</span>
                    LinkedIn
                </a>
            </div>
            
            <div class="auth-switch">
                <p>Don't have an account? <a href="#" onclick="switchToSignup()">Sign up</a></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_signup_page():
    """Create the signup page"""
    st.markdown("""
    <div class="auth-page">
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-logo">🚀</div>
                <h1 class="auth-title">Join Athena</h1>
                <p class="auth-subtitle">Create your account to get started</p>
            </div>
            
            <form class="auth-form">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label class="form-label">First Name</label>
                        <input type="text" class="form-input" placeholder="First name" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Last Name</label>
                        <input type="text" class="form-input" placeholder="Last name" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-input" placeholder="Enter your email" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Company</label>
                    <input type="text" class="form-input" placeholder="Your company name" required>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-input" placeholder="Create a password" required>
                    <button type="button" class="password-toggle">👁️</button>
                </div>
                
                <div class="form-group">
                    <label class="form-label">Confirm Password</label>
                    <input type="password" class="form-input" placeholder="Confirm your password" required>
                    <button type="button" class="password-toggle">👁️</button>
                </div>
                
                <div style="margin-bottom: 1rem;">
                    <label style="display: flex; align-items: flex-start; gap: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                        <input type="checkbox" style="margin: 0; margin-top: 0.2rem;">
                        <span>I agree to the <a href="#" style="color: var(--primary);">Terms of Service</a> and <a href="#" style="color: var(--primary);">Privacy Policy</a></span>
                    </label>
                </div>
                
                <button type="submit" class="auth-button">
                    <span class="loading-spinner" style="display: none;"></span>
                    Create Account
                </button>
            </form>
            
            <div class="auth-divider">
                <span>or sign up with</span>
            </div>
            
            <div class="social-auth">
                <a href="#" class="social-button">
                    <span>🔍</span>
                    Google
                </a>
                <a href="#" class="social-button">
                    <span>💼</span>
                    LinkedIn
                </a>
            </div>
            
            <div class="auth-switch">
                <p>Already have an account? <a href="#" onclick="switchToLogin()">Sign in</a></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def handle_demo_auth():
    """Handle demo authentication for hackathon"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: var(--bg-card); border-radius: var(--radius-xl); border: 1px solid rgba(255, 255, 255, 0.1); margin: 2rem 0;">
            <h3 style="color: var(--primary); margin-bottom: 1rem;">🎮 Demo Mode</h3>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">For the hackathon demo, you can try the application without full authentication.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🔐 Demo Login", key="demo_login", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_email = "demo@athena.ai"
                st.session_state.user_name = "Demo User"
                st.rerun()
        
        with col_b:
            if st.button("🚀 Try Without Login", key="try_demo", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_email = "guest@athena.ai"
                st.session_state.user_name = "Guest User"
                st.rerun()

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Load authentication CSS
    load_auth_css()
    
    # Page configuration
    st.set_page_config(
        page_title="Authentication - Athena",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Check if user is authenticated
    if st.session_state.get('authenticated', False):
        # Redirect to main app
        st.switch_page("🏠_Home.py")
    else:
        # Show authentication options
        auth_mode = st.session_state.get('auth_mode', 'demo')
        
        if auth_mode == 'login':
            create_login_page()
        elif auth_mode == 'signup':
            create_signup_page()
        else:
            # Show demo authentication
            handle_demo_auth()

if __name__ == "__main__":
    main() 