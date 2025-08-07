"""
📊 Athena Analytics Dashboard
Premium Analytics with Enhanced UI/UX following Frontend Action Plan
"""

import streamlit as st
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

def load_analytics_css():
    """Load additional CSS for analytics dashboard following Frontend Action Plan"""
    css = """
    <style>
    /* Analytics Dashboard Specific Styles - Following Frontend Action Plan */
    
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
    
    .analytics-container {
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
    
    /* Hero KPI Section */
    .hero-kpi {
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-kpi:hover {
        background: var(--bg-hover);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(20, 184, 166, 0.1), transparent);
        transition: all 0.6s ease;
    }
    
    .kpi-card:hover::before {
        left: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        border-color: var(--accent-positive);
    }
    
    .kpi-value {
        font-size: 48px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        animation: countUp 2s ease-out;
    }
    
    .kpi-label {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    
    .kpi-change {
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .kpi-change.positive {
        color: var(--accent-positive);
    }
    
    .kpi-change.negative {
        color: var(--accent-negative);
    }
    
    /* Filters Section */
    .filters-section {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-primary);
    }
    
    .filter-pills {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    
    .filter-pill {
        background: var(--bg-hover);
        border: 1px solid var(--border-primary);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .filter-pill:hover {
        background: var(--accent-positive);
        color: white;
        border-color: var(--accent-positive);
    }
    
    .filter-pill.active {
        background: var(--accent-positive);
        color: white;
        border-color: var(--accent-positive);
    }
    
    /* Opportunity Cards */
    .opportunity-list {
        display: grid;
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .opportunity-card {
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-primary);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .opportunity-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(20, 184, 166, 0.05), transparent);
        transition: all 0.6s ease;
    }
    
    .opportunity-card:hover::before {
        left: 100%;
    }
    
    .opportunity-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        border-color: var(--accent-positive);
    }
    
    .opportunity-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    
    .opportunity-info {
        flex: 1;
    }
    
    .opportunity-name {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .opportunity-account {
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    
    .opportunity-amount {
        font-size: 24px;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .opportunity-health {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .health-score {
        font-size: 16px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        min-width: 60px;
    }
    
    .health-score.high {
        background: rgba(20, 184, 166, 0.2);
        color: var(--accent-positive);
        border: 1px solid var(--accent-positive);
    }
    
    .health-score.medium {
        background: rgba(245, 158, 11, 0.2);
        color: var(--accent-warning);
        border: 1px solid var(--accent-warning);
    }
    
    .health-score.low {
        background: rgba(239, 68, 68, 0.2);
        color: var(--accent-negative);
        border: 1px solid var(--accent-negative);
    }
    
    .opportunity-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-primary);
    }
    
    .detail-item {
        text-align: center;
    }
    
    .detail-label {
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 0.25rem;
    }
    
    .detail-value {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    /* Animations */
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
    
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
    
    .shimmer {
        background: linear-gradient(90deg, var(--bg-hover) 25%, var(--bg-secondary) 50%, var(--bg-hover) 75%);
        background-size: 200px 100%;
        animation: shimmer 1.5s infinite;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: 1fr;
        }
        
        .opportunity-header {
            flex-direction: column;
            gap: 1rem;
        }
        
        .opportunity-details {
            grid-template-columns: repeat(2, 1fr);
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

def create_hero_kpi_section():
    """Create the Hero KPI Section with living data animations"""
    st.markdown("""
    <div class="hero-kpi">
        <h2 class="h2-text" style="margin-bottom: 1.5rem;">📈 Portfolio Overview</h2>
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Pipeline Value</div>
                <div class="kpi-value">$2.4B</div>
                <div class="kpi-change positive">
                    <span>↗</span>
                    <span>+12.5% vs last month</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Overall Pipeline Health</div>
                <div class="kpi-value">78%</div>
                <div class="kpi-change positive">
                    <span>↗</span>
                    <span>+5.2% vs last month</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Deals at Risk</div>
                <div class="kpi-value">23</div>
                <div class="kpi-change negative">
                    <span>↘</span>
                    <span>-8.3% vs last month</span>
                </div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Win Rate</div>
                <div class="kpi-value">67%</div>
                <div class="kpi-change positive">
                    <span>↗</span>
                    <span>+3.1% vs last month</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_filters_section():
    """Create the Filters Section with pill-shaped buttons"""
    st.markdown("""
    <div class="filters-section">
        <h3 class="h2-text" style="margin-bottom: 1rem;">🔍 Filters & Controls</h3>
        <div class="filter-pills">
            <div class="filter-pill active">All Stages</div>
            <div class="filter-pill">Prospecting</div>
            <div class="filter-pill">Qualification</div>
            <div class="filter-pill">Proposal</div>
            <div class="filter-pill">Negotiation</div>
            <div class="filter-pill">Closed Won</div>
            <div class="filter-pill">Closed Lost</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_opportunity_cards():
    """Create the Opportunity Cards with hover animations"""
    opportunities = [
        {
            "name": "Enterprise CRM Implementation",
            "account": "TechCorp Solutions",
            "amount": "$2.5M",
            "health_score": 85,
            "stage": "Negotiation",
            "days_in_stage": 12,
            "probability": 75
        },
        {
            "name": "Cloud Migration Project",
            "account": "Global Industries",
            "amount": "$1.8M",
            "health_score": 62,
            "stage": "Proposal",
            "days_in_stage": 8,
            "probability": 60
        },
        {
            "name": "AI Platform Integration",
            "account": "Innovate Labs",
            "amount": "$3.2M",
            "health_score": 45,
            "stage": "Qualification",
            "days_in_stage": 15,
            "probability": 40
        },
        {
            "name": "Data Analytics Suite",
            "account": "DataFlow Systems",
            "amount": "$1.2M",
            "health_score": 92,
            "stage": "Negotiation",
            "days_in_stage": 5,
            "probability": 85
        },
        {
            "name": "Security Infrastructure",
            "account": "SecureNet Corp",
            "amount": "$4.1M",
            "health_score": 38,
            "stage": "Proposal",
            "days_in_stage": 22,
            "probability": 35
        }
    ]
    
    st.markdown("""
    <div class="opportunity-list">
    """, unsafe_allow_html=True)
    
    for i, opp in enumerate(opportunities):
        health_class = "high" if opp["health_score"] >= 70 else "medium" if opp["health_score"] >= 50 else "low"
        
        st.markdown(f"""
        <div class="opportunity-card" onclick="showOpportunityDetails({i})">
            <div class="opportunity-header">
                <div class="opportunity-info">
                    <div class="opportunity-name">{opp['name']}</div>
                    <div class="opportunity-account">{opp['account']}</div>
                    <div class="opportunity-amount">{opp['amount']}</div>
                </div>
                <div class="opportunity-health">
                    <div class="health-score {health_class}">{opp['health_score']}%</div>
                </div>
            </div>
            <div class="opportunity-details">
                <div class="detail-item">
                    <div class="detail-label">Stage</div>
                    <div class="detail-value">{opp['stage']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Days in Stage</div>
                    <div class="detail-value">{opp['days_in_stage']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Probability</div>
                    <div class="detail-value">{opp['probability']}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def create_gemini_modal():
    """Create the Gemini Diagnosis Modal with shimmer effects"""
    st.markdown("""
    <div id="gemini-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(8px); z-index: 1000; display: flex; align-items: center; justify-content: center;">
        <div style="background: var(--bg-secondary); border-radius: 16px; padding: 2rem; max-width: 600px; width: 90%; border: 1px solid var(--border-primary); animation: fadeInUp 0.3s ease-out;">
            <h3 class="h2-text" style="margin-bottom: 1.5rem;">🤖 AI Diagnosis</h3>
            <div class="shimmer" style="height: 20px; border-radius: 4px; margin-bottom: 1rem;"></div>
            <div class="shimmer" style="height: 16px; border-radius: 4px; margin-bottom: 0.5rem;"></div>
            <div class="shimmer" style="height: 16px; border-radius: 4px; margin-bottom: 0.5rem;"></div>
            <div class="shimmer" style="height: 16px; border-radius: 4px; margin-bottom: 1rem;"></div>
            <div style="display: flex; gap: 1rem; margin-top: 2rem;">
                <button style="background: var(--accent-positive); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Generate Insights</button>
                <button style="background: transparent; color: var(--text-secondary); border: 1px solid var(--border-primary); padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Close</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Load analytics CSS
    load_analytics_css()
    
    # Page configuration
    st.set_page_config(
        page_title="Analytics - Athena",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        st.switch_page("auth_system.py")
    
    # Main Analytics Dashboard
    st.markdown('<h1 class="h1-text">📊 Portfolio Analytics</h1>', unsafe_allow_html=True)
    
    # Hero KPI Section
    create_hero_kpi_section()
    
    # Filters Section
    create_filters_section()
    
    # Opportunity Cards
    st.markdown('<h3 class="h2-text" style="margin-bottom: 1rem;">🎯 Opportunity Health</h3>', unsafe_allow_html=True)
    create_opportunity_cards()
    
    # Gemini Modal
    create_gemini_modal()
    
    # JavaScript for interactivity
    st.markdown("""
    <script>
    function showOpportunityDetails(index) {
        // Show Gemini modal with shimmer effect
        document.getElementById('gemini-modal').style.display = 'flex';
        
        // Simulate API call with shimmer effect
        setTimeout(() => {
            // Replace shimmer with actual content
            const modal = document.getElementById('gemini-modal');
            modal.innerHTML = `
                <div style="background: var(--bg-secondary); border-radius: 16px; padding: 2rem; max-width: 600px; width: 90%; border: 1px solid var(--border-primary); animation: fadeInUp 0.3s ease-out;">
                    <h3 class="h2-text" style="margin-bottom: 1.5rem;">🤖 AI Diagnosis</h3>
                    <div style="color: var(--text-primary); line-height: 1.6; margin-bottom: 1.5rem;">
                        <p>Based on my analysis of this opportunity, I've identified several key factors affecting its health score:</p>
                        <ul style="margin-top: 1rem;">
                            <li>Strong engagement metrics with 85% email open rates</li>
                            <li>Recent activity shows positive momentum</li>
                            <li>Competitive positioning is favorable</li>
                            <li>Stakeholder alignment appears solid</li>
                        </ul>
                        <p style="margin-top: 1rem;"><strong>Recommendation:</strong> Continue current engagement strategy while focusing on addressing the remaining technical requirements.</p>
                    </div>
                    <div style="display: flex; gap: 1rem;">
                        <button onclick="closeModal()" style="background: var(--accent-positive); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Generate Action Plan</button>
                        <button onclick="closeModal()" style="background: transparent; color: var(--text-secondary); border: 1px solid var(--border-primary); padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; cursor: pointer;">Close</button>
                    </div>
                </div>
            `;
        }, 2000);
    }
    
    function closeModal() {
        document.getElementById('gemini-modal').style.display = 'none';
    }
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()