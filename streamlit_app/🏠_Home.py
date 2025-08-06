"""
🚀 Athena: AI-Powered Sales Intelligence Platform
Main Streamlit Application - Homepage
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent / "utils"))
sys.path.append(str(Path(__file__).parent / "components"))
sys.path.append(str(Path(__file__).parent / "styles"))

# Import our custom modules
from athena_models import get_model_service, get_sample_opportunities, get_model_service_status
from charts import create_health_score_gauge, create_risk_distribution_pie
from athena_styles import (
    load_advanced_css, create_metric_card, create_feature_card,
    create_success_message, create_info_message
)

# Configure the page
st.set_page_config(
    page_title="Athena - AI Sales Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load advanced CSS with animations
load_advanced_css()

# Cached functions for better performance
@st.cache_resource
def get_cached_model_service():
    """Get cached model service instance"""
    return get_model_service()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_sample_opportunities():
    """Get cached sample opportunities"""
    return get_sample_opportunities()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cached_portfolio_analysis(_model_service, sample_opportunities):
    """Cache portfolio analysis results"""
    portfolio_data = []
    for opp in sample_opportunities:
        try:
            result = _model_service.predict_health_score(opp)
            portfolio_data.append(result)
        except Exception as e:
            # Log error but continue with other opportunities
            st.warning(f"Error analyzing opportunity {opp.get('Id', 'Unknown')}: {str(e)}")
            continue
    return portfolio_data

def main():
    # Clean Hero Section
    st.markdown('<h1 class="main-header">🚀 ATHENA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Sales Intelligence Platform</p>', unsafe_allow_html=True)
    
    # Quick Demo Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 Try Live Demo", key="demo_button", use_container_width=True):
            st.switch_page("pages/02_🎮_Live_Demo.py")
    
    st.markdown("---")
    
    # Business Impact Metrics
    st.markdown("## 📈 **Proven Business Impact**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric1 = create_metric_card("Model Performance", "+11.7%", "+11.7%")
        st.markdown(metric1, unsafe_allow_html=True)
    
    with col2:
        metric2 = create_metric_card("Win Rate", "+15%", "+15%")
        st.markdown(metric2, unsafe_allow_html=True)
    
    with col3:
        metric3 = create_metric_card("Sales Cycle", "-20%", "-20%")
        st.markdown(metric3, unsafe_allow_html=True)
    
    with col4:
        metric4 = create_metric_card("Forecast Accuracy", "85%", "+25%")
        st.markdown(metric4, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown("## 🎯 **Key Features**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        feature1 = create_feature_card(
            "Intelligent Health Scoring",
            "Advanced ensemble ML models (XGBoost + LightGBM) analyze 48+ features to predict opportunity health scores with 70% AUC accuracy.",
            "🤖"
        )
        st.markdown(feature1, unsafe_allow_html=True)
        
        feature2 = create_feature_card(
            "AI-Powered Diagnostics",
            "Google Gemini AI provides natural language insights and actionable recommendations for improving opportunity health.",
            "💡"
        )
        st.markdown(feature2, unsafe_allow_html=True)
    
    with col2:
        feature3 = create_feature_card(
            "Real-time Analytics",
            "Interactive dashboards with live portfolio health monitoring, risk distribution analysis, and performance tracking.",
            "📊"
        )
        st.markdown(feature3, unsafe_allow_html=True)
        
        feature4 = create_feature_card(
            "Automated Workflows",
            "Seamless Salesforce integration with automated rescue workflows and Slack notifications for at-risk opportunities.",
            "⚡"
        )
        st.markdown(feature4, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technology Stack
    st.markdown("## 🔬 **Advanced Technology Stack**")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("### 🤖 **Machine Learning**")
        st.markdown("""
        - **Ensemble Models**: XGBoost + LightGBM
        - **Hyperparameter Optimization**: Optuna
        - **Feature Engineering**: 48+ engineered features
        - **Model Performance**: 70% AUC accuracy
        """)
    
    with tech_col2:
        st.markdown("### 🌐 **AI Integration**")
        st.markdown("""
        - **Google Gemini API**: Natural language insights
        - **Real-time Analysis**: Live opportunity scoring
        - **Intelligent Diagnostics**: AI-powered recommendations
        - **Contextual Understanding**: Deep opportunity analysis
        """)
    
    with tech_col3:
        st.markdown("### 🏗️ **Infrastructure**")
        st.markdown("""
        - **Streamlit**: Interactive web application
        - **Supabase**: Authentication & database
        - **Salesforce**: CRM integration
        - **Slack**: Automated notifications
        """)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("## 🚀 **Ready to Transform Your Sales?**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 1rem; border: 1px solid #e2e8f0;">
            <h3 style="color: #2563eb; margin-bottom: 1rem;">Start Your Demo Today</h3>
            <p style="color: #64748b; margin-bottom: 1.5rem;">Experience the power of AI-driven sales intelligence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.875rem; padding: 1rem;">
        Built with ❤️ for the hackathon | Powered by AI & ML
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()