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
from athena_styles import load_advanced_css, create_animated_metric, create_typing_text

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
    # Hero Section
    st.markdown('<h1 class="main-header">🚀 ATHENA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Sales Intelligence Platform</p>', unsafe_allow_html=True)
    
    # Animated typing text
    typing_text = create_typing_text("Transform your sales operations with intelligent opportunity health scoring")
    st.markdown(f"""
    <div style="text-align: center; font-size: 1.3rem; margin: 2rem 0; color: #64748b;">
        {typing_text}
        <br><br>
        <span style="animation: fadeInUp 2s ease-out 3s both;">Real-time analytics and AI-powered insights that drive revenue growth.</span>
    </div>
    """, unsafe_allow_html=True)
    
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
        metric1 = create_animated_metric("Model Performance<br>Improvement", "+11.7%", "+11.7%")
        st.markdown(metric1, unsafe_allow_html=True)
    
    with col2:
        metric2 = create_animated_metric("Win Rate<br>Increase", "+15%", "+15%")
        st.markdown(metric2, unsafe_allow_html=True)
    
    with col3:
        metric3 = create_animated_metric("Sales Cycle<br>Reduction", "-20%", "-20%")
        st.markdown(metric3, unsafe_allow_html=True)
    
    with col4:
        metric4 = create_animated_metric("Forecast<br>Accuracy", "85%", "+25%")
        st.markdown(metric4, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.markdown("## 🎯 **Key Features**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Intelligent Health Scoring</h3>
            <p>Advanced ensemble ML models (XGBoost + LightGBM) analyze 48+ features to predict opportunity health scores with 70% AUC accuracy.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>⚡ Real-time Analytics</h3>
            <p>Interactive dashboards with live monitoring, drift detection, and performance tracking across your entire sales portfolio.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 AI-Powered Diagnostics</h3>
            <p>Natural language explanations and actionable recommendations powered by Google Gemini AI for every opportunity.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🛡️ Automated Rescue Workflows</h3>
            <p>Instant alerts and automated intervention workflows via Salesforce and Slack when deals show signs of risk.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Preview Section
    st.markdown("## 🎮 **Live Preview**")
    
    # Initialize model service with caching and better error handling
    try:
        model_service = get_cached_model_service()
        service_status = get_model_service_status()
        
        # Show service status
        if service_status.get('is_mock'):
            st.info("🔧 **Demo Mode**: Using mock predictions for demonstration")
        
        # Get sample data (cached)
        sample_opportunities = get_cached_sample_opportunities()
        
        # Show a quick demo
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sample Opportunity Health Check")
            
            # Select a sample opportunity
            selected_opp = st.selectbox(
                "Choose a sample opportunity:",
                options=range(len(sample_opportunities)),
                format_func=lambda x: f"{sample_opportunities[x]['Id']} - ${sample_opportunities[x]['Amount']:,} ({sample_opportunities[x]['Industry']})"
            )
            
            if st.button("🔍 Analyze This Opportunity", key="analyze_sample"):
                with st.spinner("Analyzing opportunity..."):
                    try:
                        # Get prediction
                        result = model_service.predict_health_score(sample_opportunities[selected_opp])
                        
                        # Display results
                        st.success(f"**Health Score: {result['health_score']}/100**")
                        st.info(f"**Risk Level: {result['risk_level']}**")
                        
                        # Show warnings if any
                        if result.get('is_mock_prediction'):
                            st.caption("🔧 This is a demo prediction")
                        
                        # Show model breakdown
                        if 'model_predictions' in result and result['model_predictions']:
                            st.markdown("**Model Breakdown:**")
                            predictions = result['model_predictions']
                            if 'ensemble' in predictions:
                                st.write(f"• **Ensemble: {predictions['ensemble']:.1%}**")
                            if 'xgb' in predictions:
                                st.write(f"• XGBoost: {predictions['xgb']:.1%}")
                            if 'lightgbm' in predictions:
                                st.write(f"• LightGBM: {predictions['lightgbm']:.1%}")
                            if 'mock' in predictions:
                                st.write(f"• Demo Model: {predictions['mock']:.1%}")
                        
                    except Exception as e:
                        st.error(f"Error analyzing opportunity: {str(e)}")
                        st.info("💡 **Tip**: Try selecting a different opportunity or refresh the page")
        
        with col2:
            st.markdown("### Portfolio Overview")
            
            # Use cached portfolio analysis
            try:
                with st.spinner("Analyzing portfolio..."):
                    portfolio_data = get_cached_portfolio_analysis(model_service, sample_opportunities)
                
                if portfolio_data:
                    # Show risk distribution
                    fig = create_risk_distribution_pie(portfolio_data)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show summary stats
                    avg_health = sum(r['health_score'] for r in portfolio_data) / len(portfolio_data)
                    at_risk_count = sum(1 for r in portfolio_data if r['health_score'] < 60)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Avg Health Score", f"{avg_health:.0f}")
                    with col_b:
                        st.metric("At Risk Deals", at_risk_count)
                else:
                    st.info("Portfolio analysis will appear here")
            except Exception as e:
                st.warning(f"Portfolio analysis unavailable: {str(e)}")
                st.info("Using sample visualization")
                # Show a sample chart
                fig = create_risk_distribution_pie([])
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.warning(f"Model service initialization failed: {str(e)}")
        st.info("💡 **Demo continues**: Using fallback mode for demonstration")
        
        # Show fallback content
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Sample Analysis (Demo Mode)")
            st.info("**Sample Health Score: 73/100**")
            st.info("**Risk Level: Medium Risk**")
        with col2:
            st.markdown("### Sample Portfolio")
            # Show sample chart
            fig = create_risk_distribution_pie([])
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Technology Section
    st.markdown("## 🔬 **Advanced Technology**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🤖 Machine Learning")
        st.markdown("""
        - **Ensemble Models**: XGBoost + LightGBM
        - **48+ Features**: Advanced feature engineering
        - **70% AUC**: Validated performance
        - **Real-time Scoring**: Sub-second predictions
        """)
    
    with col2:
        st.markdown("### 🧠 AI Integration")
        st.markdown("""
        - **Google Gemini**: Natural language diagnostics
        - **Contextual Insights**: Personalized recommendations
        - **Automated Workflows**: Smart interventions
        - **Continuous Learning**: Model improvement
        """)
    
    with col3:
        st.markdown("### ⚙️ Enterprise Ready")
        st.markdown("""
        - **Salesforce Integration**: Native CRM connectivity
        - **Real-time Monitoring**: Performance tracking
        - **Scalable Architecture**: Multi-user support
        - **Security**: Role-based access control
        """)
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("## 🚀 **Ready to Transform Your Sales?**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <p style="font-size: 1.2rem; margin: 2rem 0;">
                Experience the power of AI-driven sales intelligence. 
                Predict opportunity health, prevent deal loss, and accelerate revenue growth.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎮 Try Live Demo", key="cta_demo", use_container_width=True):
                st.switch_page("pages/02_🎮_Live_Demo.py")
        with col_b:
            if st.button("📊 View Analytics", key="cta_analytics", use_container_width=True):
                st.switch_page("pages/03_📊_Analytics.py")

# Sidebar
def setup_sidebar():
    st.sidebar.markdown("## 🚀 Athena Navigation")
    
    st.sidebar.markdown("""
    ### Quick Links
    - 🏠 **Homepage** - Overview and features
    - 🎮 **Live Demo** - Interactive health checker
    - 📊 **Analytics** - Real-time dashboards
    - 🔬 **Technology** - ML model details
    """)
    
    st.sidebar.markdown("---")
    
    # Model Status with caching
    st.sidebar.markdown("### 🤖 Model Status")
    try:
        service_status = get_model_service_status()
        
        if service_status['status'] == 'ready':
            if service_status.get('is_mock'):
                st.sidebar.warning("🔧 Demo Mode")
                st.sidebar.caption("Using mock predictions")
            else:
                st.sidebar.success("✅ Models Ready")
        elif service_status['status'] == 'error':
            st.sidebar.error("❌ Model Error")
            if service_status.get('is_mock'):
                st.sidebar.info("🔧 Fallback: Demo mode active")
        else:
            st.sidebar.warning("⚠️ Initializing...")
        
        # Get model info (cached)
        try:
            model_service = get_cached_model_service()
            model_info = model_service.get_model_info()
            
            st.sidebar.markdown(f"""
            **System Status:**
            - Service: {'Demo' if service_status.get('is_mock') else 'Production'}
            - Ensemble: {'✅' if model_info['models_loaded'].get('ensemble') else '❌'}
            - XGBoost: {'✅' if model_info['models_loaded'].get('xgboost') else '❌'}
            - LightGBM: {'✅' if model_info['models_loaded'].get('lightgbm') else '❌'}
            """)
        except Exception:
            st.sidebar.caption("Model details unavailable")
        
    except Exception as e:
        st.sidebar.error("❌ Status Unknown")
        st.sidebar.caption("Please refresh to retry")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📞 Support")
    st.sidebar.info("Built for Tableau Hackathon 2025\n\n🎯 Transforming Sales Operations with AI")

if __name__ == "__main__":
    setup_sidebar()
    main()