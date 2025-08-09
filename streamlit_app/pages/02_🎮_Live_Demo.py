"""
🎮 Athena Live Demo
Interactive Demo with Enhanced UI/UX following Frontend Action Plan
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import json

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import get_model_service, get_sample_opportunities
from charts import create_health_score_gauge, create_risk_distribution_pie
from athena_styles import (
    load_advanced_css, create_metric_card_3d, create_feature_card_3d,
    create_success_message_3d, create_error_message_3d, create_info_message_3d,
    add_floating_particles
)

# Load premium CSS with 3D animations
load_advanced_css()

def load_demo_css():
    """Load additional CSS for live demo following Frontend Action Plan"""
    css = """
    <style>
    /* Live Demo Specific Styles - Following Frontend Action Plan */
    
    /* Design Philosophy: Clarity First, Fluid & Responsive, "Living" Data */
    
    /* Visual Identity System - Color Palette */
    :root {
        /* Backgrounds */
        --bg-primary: #111827;
        --bg-secondary: #1F2937;
        --bg-hover: #374151;
        
        /* Text */
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --text-disabled: #4B5563;
        
        /* Accents & Status */
        --accent-positive: #14B8A6;
        --accent-warning: #F59E0B;
        --accent-negative: #EF4444;
        
        /* Borders */
        --border-primary: #374151;
    }
    
    /* Typography - Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .demo-container {
        font-family: 'Inter', sans-serif;
        background: var(--bg-primary);
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* Display Typography - 48px, Bold (700) */
    .display-text {
        font-size: 48px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
    }
    
    /* Heading 1 - 32px, Bold (700) */
    .h1-text {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.3;
    }
    
    /* Heading 2 - 24px, Semi-Bold (600) */
    .h2-text {
        font-size: 24px;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.4;
    }
    
    /* Body - 16px, Regular (400) */
    .body-text {
        font-size: 16px;
        font-weight: 400;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Caption - 12px, Regular (400) */
    .caption-text {
        font-size: 12px;
        font-weight: 400;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    /* Demo Form Section */
    .demo-form-section {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .demo-form-section:hover {
        background: var(--bg-hover);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .form-group {
        position: relative;
    }
    
    .form-label {
        display: block;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .form-input {
        width: 100%;
        background: var(--bg-hover);
        border: 2px solid var(--border-primary);
        border-radius: 8px;
        padding: 1rem;
        color: var(--text-primary);
        font-size: 16px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }
    
    .form-input:focus {
        border-color: var(--accent-positive);
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1);
        outline: none;
        background: var(--bg-secondary);
    }
    
    .form-input.error {
        border-color: var(--accent-negative);
    }
    
    .form-input.success {
        border-color: var(--accent-positive);
    }
    
    .demo-button {
        background: linear-gradient(135deg, var(--accent-positive) 0%, #0D9488 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }
    
    .demo-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: all 0.6s ease;
    }
    
    .demo-button:hover::before {
        left: 100%;
    }
    
    .demo-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(20, 184, 166, 0.3);
    }
    
    .demo-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Results Section */
    .results-section {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .results-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .health-score-display {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .score-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 700;
        color: white;
        position: relative;
    }
    
    .score-circle.high {
        background: linear-gradient(135deg, var(--accent-positive) 0%, #0D9488 100%);
    }
    
    .score-circle.medium {
        background: linear-gradient(135deg, var(--accent-warning) 0%, #D97706 100%);
    }
    
    .score-circle.low {
        background: linear-gradient(135deg, var(--accent-negative) 0%, #DC2626 100%);
    }
    
    .score-info {
        flex: 1;
    }
    
    .score-label {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 0.25rem;
    }
    
    .score-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .score-description {
        font-size: 16px;
        color: var(--text-secondary);
        line-height: 1.5;
    }
    
    /* Insights Section */
    .insights-section {
        margin-top: 2rem;
        padding-top: 2rem;
        border-top: 1px solid var(--border-primary);
    }
    
    .insight-card {
        background: var(--bg-hover);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        border-color: var(--accent-positive);
    }
    
    .insight-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .insight-icon {
        font-size: 20px;
    }
    
    .insight-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .insight-content {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.6;
    }
    
    /* Loading Animation */
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
    
    /* Animations */
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
    
    @keyframes countUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .form-grid {
            grid-template-columns: 1fr;
        }
        
        .health-score-display {
            flex-direction: column;
            text-align: center;
        }
        
        .display-text {
            font-size: 36px;
        }
        
        .h1-text {
            font-size: 28px;
        }
        
        .h2-text {
            font-size: 20px;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_demo_form():
    """Create the interactive demo form"""
    st.markdown("""
    <div class="demo-form-section">
        <h2 class="h2-text" style="margin-bottom: 1.5rem;">🎯 Opportunity Health Checker</h2>
        <p class="body-text" style="margin-bottom: 2rem; color: var(--text-secondary);">
            Enter opportunity details below to get an AI-powered health assessment and actionable insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form inputs
    col1, col2 = st.columns(2)
    
    with col1:
        opportunity_name = st.text_input(
            "Opportunity Name",
            value="Enterprise CRM Implementation",
            help="Enter the name of the opportunity"
        )
        
        account_name = st.text_input(
            "Account Name",
            value="TechCorp Solutions",
            help="Enter the account name"
        )
        
        amount = st.number_input(
            "Deal Amount ($)",
            min_value=0,
            value=2500000,
            step=100000,
            help="Enter the deal amount in dollars"
        )
        
        stage = st.selectbox(
            "Sales Stage",
            ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
            index=3,
            help="Select the current sales stage"
        )
    
    with col2:
        days_in_stage = st.number_input(
            "Days in Current Stage",
            min_value=0,
            value=12,
            help="Enter the number of days in the current stage"
        )
        
        probability = st.slider(
            "Win Probability (%)",
            min_value=0,
            max_value=100,
            value=75,
            help="Select the win probability percentage"
        )
        
        industry = st.selectbox(
            "Industry",
            ["Technology", "Healthcare", "Financial Services", "Manufacturing", "Retail", "Other"],
            index=0,
            help="Select the industry"
        )
        
        region = st.selectbox(
            "Region",
            ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"],
            index=0,
            help="Select the region"
        )
    
    # Additional fields
    col3, col4 = st.columns(2)
    
    with col3:
        email_opens = st.slider(
            "Email Open Rate (%)",
            min_value=0,
            max_value=100,
            value=85,
            help="Enter the email open rate percentage"
        )
        
        last_activity_days = st.number_input(
            "Days Since Last Activity",
            min_value=0,
            value=3,
            help="Enter the number of days since the last activity"
        )
    
    with col4:
        support_cases = st.number_input(
            "Number of Support Cases",
            min_value=0,
            value=2,
            help="Enter the number of support cases"
        )
        
        critical_issues = st.number_input(
            "Critical Issues",
            min_value=0,
            value=0,
            help="Enter the number of critical issues"
        )
    
    # Submit button
    col5, col6, col7 = st.columns([1, 2, 1])
    with col6:
        if st.button("🚀 Analyze Opportunity Health", key="analyze_button", use_container_width=True):
            return {
                "opportunity_name": opportunity_name,
                "account_name": account_name,
                "amount": amount,
                "stage": stage,
                "days_in_stage": days_in_stage,
                "probability": probability,
                "industry": industry,
                "region": region,
                "email_opens": email_opens,
                "last_activity_days": last_activity_days,
                "support_cases": support_cases,
                "critical_issues": critical_issues
            }
    
    return None

def create_results_section(opportunity_data):
    """Create the results section with health score and insights"""
    # Simulate health score calculation
    health_score = calculate_health_score(opportunity_data)
    health_class = "high" if health_score >= 70 else "medium" if health_score >= 50 else "low"
    
    st.markdown(f"""
    <div class="results-section">
        <div class="results-header">
            <h3 class="h2-text">📊 Health Analysis Results</h3>
        </div>
        
        <div class="health-score-display">
            <div class="score-circle {health_class}">
                {health_score}%
            </div>
            <div class="score-info">
                <div class="score-label">Overall Health Score</div>
                <div class="score-value">{health_score}%</div>
                <div class="score-description">
                    {get_health_description(health_score)}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create insights
    insights = generate_insights(opportunity_data, health_score)
    
    st.markdown("""
    <div class="insights-section">
        <h4 class="h2-text" style="margin-bottom: 1rem;">💡 AI-Powered Insights</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-header">
                <span class="insight-icon">{insight['icon']}</span>
                <span class="insight-title">{insight['title']}</span>
            </div>
            <div class="insight-content">
                {insight['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def calculate_health_score(data):
    """Calculate health score based on opportunity data"""
    score = 50  # Base score
    
    # Stage impact
    stage_scores = {
        "Prospecting": 30,
        "Qualification": 45,
        "Proposal": 60,
        "Negotiation": 75,
        "Closed Won": 100,
        "Closed Lost": 0
    }
    score += stage_scores.get(data["stage"], 50) - 50
    
    # Probability impact
    score += (data["probability"] - 50) * 0.3
    
    # Email engagement impact
    score += (data["email_opens"] - 50) * 0.2
    
    # Activity impact
    if data["last_activity_days"] <= 3:
        score += 10
    elif data["last_activity_days"] <= 7:
        score += 5
    else:
        score -= 10
    
    # Support impact
    score -= data["support_cases"] * 5
    score -= data["critical_issues"] * 15
    
    # Days in stage impact
    if data["days_in_stage"] <= 7:
        score += 5
    elif data["days_in_stage"] >= 30:
        score -= 10
    
    return max(0, min(100, int(score)))

def get_health_description(score):
    """Get health score description"""
    if score >= 80:
        return "Excellent health - Strong likelihood of closing successfully"
    elif score >= 60:
        return "Good health - On track but needs attention to key areas"
    elif score >= 40:
        return "Moderate health - Requires immediate attention and intervention"
    else:
        return "Poor health - High risk of loss, needs urgent rescue strategy"

def generate_insights(data, health_score):
    """Generate AI-powered insights"""
    insights = []
    
    # Stage insights
    if data["stage"] == "Negotiation" and health_score < 70:
        insights.append({
            "icon": "⚠️",
            "title": "Negotiation Risk",
            "content": "This opportunity is in negotiation but shows signs of risk. Focus on addressing stakeholder concerns and competitive positioning."
        })
    
    # Activity insights
    if data["last_activity_days"] > 7:
        insights.append({
            "icon": "⏰",
            "title": "Activity Gap",
            "content": f"It's been {data['last_activity_days']} days since the last activity. Schedule immediate follow-up to maintain momentum."
        })
    
    # Engagement insights
    if data["email_opens"] >= 80:
        insights.append({
            "icon": "📧",
            "title": "Strong Engagement",
            "content": f"Excellent email engagement at {data['email_opens']}% open rate. Leverage this momentum for next steps."
        })
    elif data["email_opens"] < 50:
        insights.append({
            "icon": "📧",
            "title": "Low Engagement",
            "content": f"Email engagement is low at {data['email_opens']}%. Consider different communication strategies."
        })
    
    # Support insights
    if data["support_cases"] > 0:
        insights.append({
            "icon": "🛠️",
            "title": "Support Issues",
            "content": f"{data['support_cases']} support cases may indicate implementation challenges. Address these proactively."
        })
    
    # Critical issues
    if data["critical_issues"] > 0:
        insights.append({
            "icon": "🚨",
            "title": "Critical Issues",
            "content": f"{data['critical_issues']} critical issues detected. These must be resolved immediately to prevent deal loss."
        })
    
    # General recommendations
    if health_score >= 80:
        insights.append({
            "icon": "✅",
            "title": "Excellent Position",
            "content": "This opportunity is in excellent health. Continue current strategy and focus on closing timeline."
        })
    elif health_score < 40:
        insights.append({
            "icon": "🚨",
            "title": "Rescue Strategy Needed",
            "content": "This opportunity requires immediate intervention. Consider executive sponsorship and revised approach."
        })
    
    return insights

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Load demo CSS
    load_demo_css()
    
    # Page configuration
    st.set_page_config(
        page_title="Live Demo - Athena",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.switch_page("auth_system.py")
    
    # Main Demo Page
    st.markdown('<h1 class="h1-text">🎮 Live Demo</h1>', unsafe_allow_html=True)
    st.markdown('<p class="body-text" style="color: var(--text-secondary); margin-bottom: 2rem;">Experience Athena\'s AI-powered opportunity health analysis in real-time.</p>', unsafe_allow_html=True)
    
    # Demo form
    opportunity_data = create_demo_form()
    
    # Show results if form submitted
    if opportunity_data:
        create_results_section(opportunity_data)

if __name__ == "__main__":
    main()