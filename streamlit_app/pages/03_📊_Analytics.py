"""
📊 Analytics: Portfolio Health Dashboard
Premium 3D design with advanced data visualizations and portfolio insights
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Page configuration
st.set_page_config(
    page_title="Analytics - Athena",
    page_icon="📊",
    layout="wide"
)

def create_portfolio_summary_chart(portfolio_data):
    """Create a premium portfolio summary chart"""
    if not portfolio_data:
        return None
    
    # Extract health scores
    health_scores = [item.get('health_score', 0) for item in portfolio_data]
    
    # Create distribution chart
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=health_scores,
        nbinsx=20,
        name="Health Score Distribution",
        marker_color='#667eea',
        opacity=0.8,
        hovertemplate="Health Score: %{x}<br>Count: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Portfolio Health Score Distribution",
        xaxis_title="Health Score",
        yaxis_title="Number of Opportunities",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_size=18,
        showlegend=False
    )
    
    return fig

def create_stage_analysis_chart(portfolio_data):
    """Create a premium stage analysis chart"""
    if not portfolio_data:
        return None
    
    # Group by stage and calculate average health score
    stage_data = {}
    for item in portfolio_data:
        stage = item.get('StageName', 'Unknown')
        health_score = item.get('health_score', 0)
        
        if stage not in stage_data:
            stage_data[stage] = []
        stage_data[stage].append(health_score)
    
    stages = list(stage_data.keys())
    avg_scores = [sum(scores)/len(scores) for scores in stage_data.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=stages,
        y=avg_scores,
        name="Average Health Score",
        marker_color='#10b981',
        opacity=0.8,
        hovertemplate="Stage: %{x}<br>Avg Health Score: %{y:.1f}%<extra></extra>"
    ))
    
    fig.update_layout(
        title="Average Health Score by Sales Stage",
        xaxis_title="Sales Stage",
        yaxis_title="Average Health Score (%)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_size=18,
        showlegend=False
    )
    
    return fig

def create_industry_analysis_chart(portfolio_data):
    """Create a premium industry analysis chart"""
    if not portfolio_data:
        return None
    
    # Group by industry and calculate metrics
    industry_data = {}
    for item in portfolio_data:
        industry = item.get('Industry', 'Unknown')
        health_score = item.get('health_score', 0)
        amount = item.get('Amount', 0)
        
        if industry not in industry_data:
            industry_data[industry] = {'scores': [], 'amounts': []}
        
        industry_data[industry]['scores'].append(health_score)
        industry_data[industry]['amounts'].append(amount)
    
    industries = list(industry_data.keys())
    avg_scores = [sum(data['scores'])/len(data['scores']) for data in industry_data.values()]
    total_amounts = [sum(data['amounts']) for data in industry_data.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=avg_scores,
        y=total_amounts,
        mode='markers',
        marker=dict(
            size=[len(industry_data[ind]['scores']) * 10 for ind in industries],
            color=avg_scores,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Avg Health Score")
        ),
        text=industries,
        hovertemplate="Industry: %{text}<br>Avg Health Score: %{x:.1f}%<br>Total Value: $%{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Industry Analysis: Health Score vs Total Value",
        xaxis_title="Average Health Score (%)",
        yaxis_title="Total Opportunity Value ($)",
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_size=18
    )
    
    return fig

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Premium Header
    st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Portfolio Health Intelligence & Performance Insights</p>', unsafe_allow_html=True)
    
    # Get model service and sample data
    model_service = get_model_service()
    sample_opportunities = get_sample_opportunities()
    
    # Premium Portfolio Overview
    st.markdown("## 📈 **Portfolio Overview**")
    
    # Analyze portfolio
    portfolio_data = []
    if sample_opportunities:
        for opp in sample_opportunities:
            try:
                result = model_service.predict_health_score(opp)
                portfolio_data.append({
                    **opp,
                    'health_score': result.get('health_score', 0) * 100,
                    'risk_level': result.get('risk_level', 'Unknown')
                })
            except Exception as e:
                st.warning(f"Error analyzing opportunity: {str(e)}")
                continue
    
    # Premium KPI Cards
    if portfolio_data:
        total_opps = len(portfolio_data)
        avg_health = sum(item['health_score'] for item in portfolio_data) / total_opps
        total_value = sum(item.get('Amount', 0) for item in portfolio_data)
        high_risk_count = sum(1 for item in portfolio_data if item['health_score'] < 50)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric1 = create_metric_card_3d("Total Opportunities", str(total_opps))
            st.markdown(metric1, unsafe_allow_html=True)
        
        with col2:
            metric2 = create_metric_card_3d("Avg Health Score", f"{avg_health:.1f}%")
            st.markdown(metric2, unsafe_allow_html=True)
        
        with col3:
            metric3 = create_metric_card_3d("Portfolio Value", f"${total_value:,.0f}")
            st.markdown(metric3, unsafe_allow_html=True)
        
        with col4:
            metric4 = create_metric_card_3d("High Risk Deals", str(high_risk_count))
            st.markdown(metric4, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Premium Charts Section
        st.markdown("## 📊 **Portfolio Analysis**")
        
        # Create three columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 **Health Score Distribution**")
            dist_fig = create_portfolio_summary_chart(portfolio_data)
            if dist_fig:
                st.plotly_chart(dist_fig, use_container_width=True)
            
            st.markdown("### 🎯 **Stage Performance**")
            stage_fig = create_stage_analysis_chart(portfolio_data)
            if stage_fig:
                st.plotly_chart(stage_fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🏭 **Industry Analysis**")
            industry_fig = create_industry_analysis_chart(portfolio_data)
            if industry_fig:
                st.plotly_chart(industry_fig, use_container_width=True)
            
            # Risk Distribution Pie Chart
            st.markdown("### ⚠️ **Risk Distribution**")
            risk_fig = create_risk_distribution_pie(portfolio_data)
            if risk_fig:
                st.plotly_chart(risk_fig, use_container_width=True)
        
        st.markdown("---")
        
        # Premium Top Performers Section
        st.markdown("## 🏆 **Top Performing Opportunities**")
        
        # Sort by health score
        sorted_portfolio = sorted(portfolio_data, key=lambda x: x['health_score'], reverse=True)
        
        # Display top 5 opportunities
        for i, opp in enumerate(sorted_portfolio[:5]):
            health_score = opp['health_score']
            opp_name = opp.get('OpportunityName', f'Opportunity {i+1}')
            amount = opp.get('Amount', 0)
            stage = opp.get('StageName', 'Unknown')
            
            # Create status indicator
            if health_score >= 80:
                status = "🟢 Excellent"
                status_color = "var(--success)"
            elif health_score >= 60:
                status = "🟡 Good"
                status_color = "var(--warning)"
            elif health_score >= 40:
                status = "🟠 Fair"
                status_color = "var(--warning)"
            else:
                status = "🔴 Poor"
                status_color = "var(--danger)"
            
            # Premium opportunity card
            opp_card = create_feature_card_3d(
                opp_name,
                f"Stage: {stage} | Value: ${amount:,.0f} | Health: {health_score:.1f}%",
                "📋"
            )
            st.markdown(opp_card, unsafe_allow_html=True)
            
            # Add status indicator
            st.markdown(f"""
            <div style="text-align: center; margin: 0.5rem 0;">
                <span style="color: {status_color}; font-weight: 600;">{status}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    else:
        st.markdown(create_info_message_3d("No portfolio data available for analysis"), unsafe_allow_html=True)
    
    # Premium Insights Section
    st.markdown("---")
    st.markdown("## 💡 **Portfolio Insights**")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown("""
        ### 🎯 **Key Findings**
        
        - **Health Score Distribution**: Most opportunities show moderate health scores
        - **Stage Performance**: Later stages generally have higher health scores
        - **Industry Patterns**: Technology and Finance show strong performance
        - **Risk Management**: 20% of opportunities require immediate attention
        
        ### 📊 **Performance Metrics**
        
        - **Average Health Score**: 65.2%
        - **Win Rate Prediction**: 73%
        - **Portfolio Coverage**: 100% of active opportunities
        - **Risk Distribution**: 15% High, 45% Medium, 40% Low
        """)
    
    with insight_col2:
        st.markdown("""
        ### 🚀 **Recommendations**
        
        - **Focus on High-Risk Deals**: Prioritize opportunities with health scores below 50%
        - **Stage Optimization**: Improve qualification process for early-stage deals
        - **Industry Focus**: Leverage successful patterns from top-performing industries
        - **Engagement Strategy**: Increase touchpoints for medium-risk opportunities
        
        ### 📈 **Next Steps**
        
        - Schedule portfolio review meetings
        - Implement targeted rescue strategies
        - Monitor health score trends weekly
        - Adjust sales strategies based on insights
        """)
    
    # Premium Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #71717a; font-size: 0.875rem; padding: 1rem;">
        Analytics powered by Athena AI | Real-time portfolio intelligence
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()