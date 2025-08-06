"""
📊 Analytics Dashboard - Real-time Sales Intelligence
Comprehensive analytics and insights for sales performance
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import get_model_service, get_sample_opportunities, get_model_service_status
from charts import (
    create_health_trend_chart, create_risk_distribution_pie, 
    create_feature_importance_chart, create_industry_performance_chart,
    create_deal_value_vs_health_scatter, create_rescue_impact_chart
)
from athena_styles import load_advanced_css, create_animated_metric

# Cached functions for better performance
@st.cache_resource
def get_cached_model_service():
    """Get cached model service instance"""
    return get_model_service()

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_cached_analytics_data(_model_service):
    """Cache analytics computations"""
    sample_opportunities = get_sample_opportunities()
    portfolio_data = []
    
    for opp in sample_opportunities:
        try:
            result = _model_service.predict_health_score(opp)
            portfolio_data.append(result)
        except Exception:
            continue
    
    return portfolio_data

# Configure the page
st.set_page_config(
    page_title="Athena - Analytics",
    page_icon="📊",
    layout="wide"
)

# Load advanced CSS with animations
load_advanced_css()

def main():
    st.markdown('<h1 class="analytics-header">📊 Sales Intelligence Analytics</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: #666;">
        Real-time insights and performance metrics for your sales pipeline
    </div>
    """, unsafe_allow_html=True)
    
    # Time period selector with enhanced auto-refresh
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown("### 📅 **Analysis Period**")
    with col2:
        time_period = st.selectbox("Time Range", ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"])
    with col3:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True, help="Automatically refresh data")
    with col4:
        if auto_refresh:
            refresh_interval = st.slider("⏱️ Interval (sec)", 5, 30, 10, help="Refresh interval in seconds")
        else:
            refresh_interval = 10
    
    st.markdown("---")
    
    # Auto-refresh functionality
    if auto_refresh:
        # Add a placeholder for the countdown
        countdown_placeholder = st.empty()
        
        # Use JavaScript to create a countdown timer
        st.markdown(f"""
        <script>
        let timeLeft = {refresh_interval};
        const countdownElement = document.querySelector('.countdown');
        if (countdownElement) {{
            const timer = setInterval(() => {{
                timeLeft--;
                countdownElement.textContent = `Refreshing in ${{timeLeft}}s`;
                if (timeLeft <= 0) {{
                    clearInterval(timer);
                    window.location.reload();
                }}
            }}, 1000);
        }}
        </script>
        """, unsafe_allow_html=True)
        
        # Show refresh status
        with countdown_placeholder:
            st.info(f"🔄 Auto-refresh active - Next refresh in {refresh_interval} seconds")
    
    # Initialize model service with caching
    try:
        model_service = get_cached_model_service()
        service_status = get_model_service_status()
        
        if service_status.get('is_mock'):
            st.info("🔧 **Demo Mode**: Analytics using mock data for demonstration")
        
        model_loaded = True
        
    except Exception as e:
        st.warning(f"⚠️ Model service unavailable: {str(e)}")
        st.info("💡 **Fallback**: Showing sample analytics")
        model_loaded = False
    
    # KPI Section
    # Real-time status indicator
    if auto_refresh:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #4CAF50, #45a049); color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">
            🟢 <strong>Live Mode</strong> - Data refreshing automatically
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(90deg, #ff9800, #f57c00); color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">
            🟡 <strong>Static Mode</strong> - Data updated manually
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 🎯 **Key Performance Indicators**")
    
    # Generate sample KPI data
    kpi_data = generate_kpi_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h2>{kpi_data['total_opportunities']}</h2>
            <p>Total Opportunities</p>
            <small>+{kpi_data['opp_growth']}% from last month</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h2>{kpi_data['avg_health']:.1f}</h2>
            <p>Average Health Score</p>
            <small>+{kpi_data['health_trend']:+.1f} from last period</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h2>${kpi_data['pipeline_value']:,.0f}</h2>
            <p>Pipeline Value</p>
            <small>+{kpi_data['pipeline_growth']:.1f}% growth</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h2>{kpi_data['at_risk_deals']}</h2>
            <p>At-Risk Deals</p>
            <small>${kpi_data['at_risk_value']:,.0f} value</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 📈 **Health Score Trends**")
        
        # Health trend chart
        health_trend_fig = create_health_trend_chart(30)
        st.plotly_chart(health_trend_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 **Risk Distribution**")
        
        # Risk distribution chart
        sample_opportunities = get_sample_opportunities()
        if model_loaded:
            try:
                portfolio_data = []
                for opp in sample_opportunities:
                    result = model_service.predict_health_score(opp)
                    portfolio_data.append(result)
                risk_fig = create_risk_distribution_pie(portfolio_data)
            except:
                risk_fig = create_risk_distribution_pie([])
        else:
            risk_fig = create_risk_distribution_pie([])
        
        st.plotly_chart(risk_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Importance and Industry Performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🔬 **Feature Importance**")
        
        if model_loaded:
            feature_fig = create_feature_importance_chart(model_service)
        else:
            feature_fig = create_feature_importance_chart(None)
        
        st.plotly_chart(feature_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🏭 **Performance by Industry**")
        
        industry_fig = create_industry_performance_chart()
        st.plotly_chart(industry_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced Analytics
    st.markdown("## 🚀 **Advanced Analytics**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 💰 **Deal Value vs Health Score**")
        
        scatter_fig = create_deal_value_vs_health_scatter()
        st.plotly_chart(scatter_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### 🛡️ **Rescue Intervention Impact**")
        
        rescue_fig = create_rescue_impact_chart()
        st.plotly_chart(rescue_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights Panel
    st.markdown("## 🧠 **AI-Powered Insights**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="insight-panel">', unsafe_allow_html=True)
        st.markdown("### 🎯 **Opportunity Insights**")
        st.markdown("""
        • **23 high-value deals** require immediate attention
        • **Technology sector** showing strongest performance
        • **Average deal cycle** decreased by 12% this quarter
        • **Engagement scores** correlate strongly with win rate
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-panel">', unsafe_allow_html=True)
        st.markdown("### ⚠️ **Risk Alerts**")
        st.markdown("""
        • **15 deals** haven't been touched in 14+ days
        • **8 opportunities** have critical support cases
        • **Healthcare sector** deals taking 20% longer
        • **Q4 pipeline** needs $2M more to hit target
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="insight-panel">', unsafe_allow_html=True)
        st.markdown("### 💡 **Recommendations**")
        st.markdown("""
        • **Focus on Technology deals** in Q4 push
        • **Increase touchpoints** for stalled opportunities  
        • **Deploy rescue workflows** for at-risk deals
        • **Accelerate Healthcare** pipeline development
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Table
    st.markdown("## 📋 **Opportunity Portfolio**")
    
    # Generate sample opportunity data
    portfolio_df = generate_portfolio_data(model_service if model_loaded else None)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_filter = st.multiselect("Risk Level", 
                                   ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"],
                                   default=["Medium Risk", "High Risk", "Critical Risk"])
    
    with col2:
        industry_filter = st.multiselect("Industry", 
                                       portfolio_df['Industry'].unique(),
                                       default=portfolio_df['Industry'].unique())
    
    with col3:
        min_amount = st.number_input("Min Deal Size ($)", value=0, step=50000)
    
    with col4:
        stage_filter = st.multiselect("Sales Stage",
                                    portfolio_df['Stage'].unique(),
                                    default=portfolio_df['Stage'].unique())
    
    # Apply filters
    filtered_df = portfolio_df[
        (portfolio_df['Risk Level'].isin(risk_filter)) &
        (portfolio_df['Industry'].isin(industry_filter)) &
        (portfolio_df['Amount'] >= min_amount) &
        (portfolio_df['Stage'].isin(stage_filter))
    ]
    
    # Display filtered data
    st.dataframe(
        filtered_df,
        use_container_width=True,
        column_config={
            "Health Score": st.column_config.ProgressColumn(
                "Health Score",
                help="Opportunity health score (0-100)",
                min_value=0,
                max_value=100,
            ),
            "Amount": st.column_config.NumberColumn(
                "Amount",
                help="Deal value in USD",
                format="$%d",
            ),
        }
    )
    
    # Summary stats for filtered data
    if not filtered_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Filtered Opportunities", len(filtered_df))
        with col2:
            st.metric("Total Value", f"${filtered_df['Amount'].sum():,.0f}")
        with col3:
            st.metric("Avg Health Score", f"{filtered_df['Health Score'].mean():.1f}")
        with col4:
            avg_days = filtered_df['Days in Stage'].mean()
            st.metric("Avg Days in Stage", f"{avg_days:.0f}")

def generate_kpi_data():
    """Generate sample KPI data"""
    np.random.seed(42)
    return {
        'total_opportunities': 247,
        'opp_growth': 12,
        'avg_health': 67.3,
        'health_trend': 2.4,
        'pipeline_value': 45200000,
        'pipeline_growth': 8.7,
        'at_risk_deals': 43,
        'at_risk_value': 8900000
    }

def generate_portfolio_data(model_service):
    """Generate sample portfolio data"""
    np.random.seed(42)
    
    # Base data
    opportunities = []
    industries = ["Technology", "Healthcare", "Financial Services", "Manufacturing", "Retail"]
    stages = ["Prospecting", "Qualification", "Needs Analysis", "Proposal", "Negotiation"]
    regions = ["North America", "Europe", "Asia Pacific"]
    
    for i in range(50):
        opp_data = {
            'Id': f'OPP-{1000 + i}',
            'Amount': np.random.exponential(250000),
            'StageName': np.random.choice(stages),
            'Industry': np.random.choice(industries),
            'Region': np.random.choice(regions),
            'DaysInStage': np.random.randint(1, 120),
            'EmailOpens': np.random.randint(0, 50),
            'EmailClicks': np.random.randint(0, 20),
            'ContentDownloads': np.random.randint(0, 10),
            'MeetingsScheduled': np.random.randint(0, 15),
            'CallsMade': np.random.randint(0, 30),
            'SupportCases': np.random.randint(0, 5),
            'CriticalCases': np.random.randint(0, 2),
            'AvgCaseAge': np.random.randint(0, 30),
            'CloseDatePushed': np.random.randint(0, 3),
            'LastActivityDays': np.random.randint(0, 60),
            'CommunicationFrequency': np.random.randint(1, 15)
        }
        
        # Get health score if model is available
        if model_service:
            try:
                result = model_service.predict_health_score(opp_data)
                health_score = result['health_score']
                risk_level = result['risk_level']
            except:
                health_score = np.random.randint(20, 95)
                risk_level = "Medium Risk"
        else:
            health_score = np.random.randint(20, 95)
            if health_score >= 80:
                risk_level = "Low Risk"
            elif health_score >= 60:
                risk_level = "Medium Risk"
            elif health_score >= 40:
                risk_level = "High Risk"
            else:
                risk_level = "Critical Risk"
        
        opportunities.append({
            'Opportunity ID': opp_data['Id'],
            'Amount': int(opp_data['Amount']),
            'Stage': opp_data['StageName'],
            'Industry': opp_data['Industry'],
            'Region': opp_data['Region'],
            'Health Score': health_score,
            'Risk Level': risk_level,
            'Days in Stage': opp_data['DaysInStage'],
            'Last Activity': f"{opp_data['LastActivityDays']} days ago"
        })
    
    return pd.DataFrame(opportunities)

if __name__ == "__main__":
    main()