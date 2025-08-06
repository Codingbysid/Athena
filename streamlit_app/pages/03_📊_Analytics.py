"""
📊 Analytics - Portfolio Health Dashboard
Real-time analytics and insights for sales intelligence
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import get_model_service, get_sample_opportunities, get_model_service_status
from charts import create_health_score_gauge, create_risk_distribution_pie
from athena_styles import (
    load_advanced_css, create_metric_card, create_feature_card,
    create_success_message, create_error_message, create_info_message
)

# Configure the page
st.set_page_config(
    page_title="Athena - Analytics",
    page_icon="📊",
    layout="wide"
)

# Load advanced CSS
load_advanced_css()

def main():
    st.markdown('<h1 class="main-header">📊 Portfolio Analytics</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: #64748b;">
        Real-time insights into your sales portfolio health and performance
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize model service
    try:
        model_service = get_model_service()
        service_status = get_model_service_status()
        
        if service_status['status'] == 'error':
            if service_status['is_mock']:
                st.markdown(create_info_message("🔧 **Demo Mode**: Using mock data for analytics"), unsafe_allow_html=True)
                model_loaded = True
            else:
                st.markdown(create_error_message(f"❌ **Model Error**: {service_status['error']}"), unsafe_allow_html=True)
                model_loaded = False
        else:
            model_loaded = True
            if service_status.get('is_mock'):
                st.markdown(create_info_message("🔧 Running analytics with demo data"), unsafe_allow_html=True)
                
    except Exception as e:
        st.markdown(create_error_message(f"❌ **Unexpected Error**: {str(e)}"), unsafe_allow_html=True)
        model_loaded = False
    
    # Portfolio Overview Metrics
    st.markdown("## 📈 **Portfolio Overview**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric1 = create_metric_card("Total Opportunities", "1,247", "+12%")
        st.markdown(metric1, unsafe_allow_html=True)
    
    with col2:
        metric2 = create_metric_card("Avg Health Score", "73.2", "+5.1%")
        st.markdown(metric2, unsafe_allow_html=True)
    
    with col3:
        metric3 = create_metric_card("At Risk Deals", "89", "-8%")
        st.markdown(metric3, unsafe_allow_html=True)
    
    with col4:
        metric4 = create_metric_card("Win Rate", "68.5%", "+3.2%")
        st.markdown(metric4, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 **Health Score Distribution**")
        
        # Create sample health score distribution
        health_scores = np.random.normal(73, 15, 1000)
        health_scores = np.clip(health_scores, 0, 100)
        
        fig_dist = px.histogram(
            x=health_scores,
            nbins=20,
            title="Portfolio Health Score Distribution",
            labels={'x': 'Health Score', 'y': 'Number of Opportunities'},
            color_discrete_sequence=['#2563eb']
        )
        
        fig_dist.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("### ⚠️ **Risk Level Breakdown**")
        
        # Create risk distribution pie chart
        risk_data = {
            'Low Risk': 45,
            'Medium Risk': 35,
            'High Risk': 20
        }
        
        fig_risk = px.pie(
            values=list(risk_data.values()),
            names=list(risk_data.keys()),
            title="Opportunity Risk Distribution",
            color_discrete_sequence=['#059669', '#d97706', '#dc2626']
        )
        
        fig_risk.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    st.markdown("---")
    
    # Industry Analysis
    st.markdown("## 🏭 **Industry Performance**")
    
    # Sample industry data
    industry_data = {
        'Technology': {'count': 342, 'avg_health': 78.5, 'win_rate': 72.3},
        'Healthcare': {'count': 189, 'avg_health': 71.2, 'win_rate': 65.8},
        'Finance': {'count': 156, 'avg_health': 75.8, 'win_rate': 68.9},
        'Manufacturing': {'count': 234, 'avg_health': 69.4, 'win_rate': 62.1},
        'Retail': {'count': 98, 'avg_health': 66.7, 'win_rate': 58.4},
        'Education': {'count': 67, 'avg_health': 72.1, 'win_rate': 64.2}
    }
    
    # Create industry performance chart
    industries = list(industry_data.keys())
    health_scores = [industry_data[ind]['avg_health'] for ind in industries]
    win_rates = [industry_data[ind]['win_rate'] for ind in industries]
    
    fig_industry = go.Figure()
    
    fig_industry.add_trace(go.Bar(
        x=industries,
        y=health_scores,
        name='Avg Health Score',
        marker_color='#2563eb'
    ))
    
    fig_industry.add_trace(go.Bar(
        x=industries,
        y=win_rates,
        name='Win Rate (%)',
        marker_color='#059669'
    ))
    
    fig_industry.update_layout(
        title="Industry Performance Comparison",
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_industry, use_container_width=True)
    
    # Stage Analysis
    st.markdown("## 📊 **Pipeline Stage Analysis**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 **Stage Progression**")
        
        # Sample stage data
        stage_data = {
            'Prospecting': 156,
            'Qualification': 234,
            'Proposal': 189,
            'Negotiation': 145,
            'Closed Won': 423,
            'Closed Lost': 100
        }
        
        fig_stage = px.bar(
            x=list(stage_data.keys()),
            y=list(stage_data.values()),
            title="Opportunities by Stage",
            color_discrete_sequence=['#2563eb']
        )
        
        fig_stage.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_stage, use_container_width=True)
    
    with col2:
        st.markdown("### ⏱️ **Stage Velocity**")
        
        # Sample velocity data
        velocity_data = {
            'Prospecting': 12,
            'Qualification': 18,
            'Proposal': 25,
            'Negotiation': 15
        }
        
        fig_velocity = px.bar(
            x=list(velocity_data.keys()),
            y=list(velocity_data.values()),
            title="Average Days in Stage",
            color_discrete_sequence=['#d97706']
        )
        
        fig_velocity.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig_velocity, use_container_width=True)
    
    st.markdown("---")
    
    # Top Performers
    st.markdown("## 🏆 **Top Performing Opportunities**")
    
    # Sample top performers data
    top_performers = [
        {'id': 'DEMO001', 'name': 'TechCorp Enterprise', 'amount': 250000, 'health': 95, 'stage': 'Negotiation'},
        {'id': 'DEMO002', 'name': 'HealthPlus Solutions', 'amount': 180000, 'health': 92, 'stage': 'Proposal'},
        {'id': 'DEMO003', 'name': 'FinanceFlow Inc', 'amount': 320000, 'health': 89, 'stage': 'Negotiation'},
        {'id': 'DEMO004', 'name': 'ManufacturePro', 'amount': 150000, 'health': 87, 'stage': 'Proposal'},
        {'id': 'DEMO005', 'name': 'RetailTech Systems', 'amount': 95000, 'health': 85, 'stage': 'Qualification'}
    ]
    
    # Create top performers table
    df_top = pd.DataFrame(top_performers)
    
    st.dataframe(
        df_top,
        column_config={
            "id": "Opportunity ID",
            "name": "Company Name",
            "amount": st.column_config.NumberColumn("Amount ($)", format="$%d"),
            "health": st.column_config.NumberColumn("Health Score", format="%d"),
            "stage": "Stage"
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Insights and Recommendations
    st.markdown("## 💡 **Portfolio Insights**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 **Key Findings**")
        st.markdown("""
        - **Technology sector** shows the highest health scores (78.5 avg)
        - **Retail opportunities** need immediate attention (66.7 avg health)
        - **Proposal stage** has the highest opportunity count (189 deals)
        - **Negotiation stage** shows strong progression velocity
        """)
    
    with col2:
        st.markdown("### 🚀 **Recommendations**")
        st.markdown("""
        - **Focus on retail sector** with targeted engagement strategies
        - **Accelerate proposal stage** deals with enhanced value propositions
        - **Maintain technology momentum** with best practice sharing
        - **Optimize qualification process** to improve early-stage health scores
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.875rem; padding: 1rem;">
        Analytics updated in real-time | Powered by Athena AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()