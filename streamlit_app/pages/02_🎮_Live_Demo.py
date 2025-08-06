"""
🎮 Live Demo - Interactive Opportunity Health Checker
Real-time opportunity health scoring with AI-powered insights
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import (
    get_model_service, get_sample_opportunities, get_model_service_status,
    AthenaModelError, ModelLoadError, PredictionError, DataValidationError
)
from charts import create_health_score_gauge
from athena_styles import (
    load_advanced_css, create_success_message, create_error_message, 
    create_info_message, create_loading_spinner
)

# Configure the page
st.set_page_config(
    page_title="Athena - Live Demo",
    page_icon="🎮",
    layout="wide"
)

# Load advanced CSS with animations
load_advanced_css()

def main():
    st.markdown('<h1 class="main-header">🎮 Live Opportunity Health Checker</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: #64748b;">
        Input your opportunity details below and get instant AI-powered health insights
    </div>
    """, unsafe_allow_html=True)
    
    # Demo mode controls
    col_demo1, col_demo2, col_demo3 = st.columns(3)
    with col_demo1:
        demo_mode = st.checkbox("🎮 Demo Mode", value=True, help="Enable interactive demo features")
    with col_demo2:
        if demo_mode:
            auto_demo = st.checkbox("🔄 Auto Demo", value=False, help="Automatically cycle through sample opportunities")
    with col_demo3:
        if demo_mode and auto_demo:
            demo_speed = st.slider("⚡ Demo Speed", 1, 10, 3, help="Seconds between demo cycles")
    
    # Initialize model service with enhanced error handling
    try:
        model_service = get_model_service()
        service_status = get_model_service_status()
        
        if service_status['status'] == 'error':
            if service_status['is_mock']:
                st.markdown(create_info_message("🔧 **Demo Mode**: Using mock predictions (real models unavailable)"), unsafe_allow_html=True)
                model_loaded = True
            else:
                st.markdown(create_error_message(f"❌ **Model Error**: {service_status['error']}"), unsafe_allow_html=True)
                model_loaded = False
        else:
            model_loaded = True
            if service_status.get('is_mock'):
                st.markdown(create_info_message("🔧 Running in demo mode with mock predictions"), unsafe_allow_html=True)
                
    except Exception as e:
        st.markdown(create_error_message(f"❌ **Unexpected Error**: {str(e)}"), unsafe_allow_html=True)
        st.markdown(create_info_message("💡 **Troubleshooting**: Please check that model files are in the correct location"), unsafe_allow_html=True)
        model_loaded = False
    
    # Main layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 **Opportunity Details**")
        
        # Quick load sample data
        sample_opportunities = get_sample_opportunities()
        
        st.markdown("**Quick Start:**")
        sample_choice = st.selectbox(
            "Load sample opportunity:",
            options=["Custom Entry"] + [f"{opp['Id']} - ${opp['Amount']:,}" for opp in sample_opportunities],
            key="sample_selector"
        )
        
        # Initialize default values
        if sample_choice != "Custom Entry":
            idx = int(sample_choice.split(" - ")[0].replace("DEMO00", "")) - 1
            selected_opp = sample_opportunities[idx]
        else:
            selected_opp = {
                'Id': 'CUSTOM001',
                'Amount': 50000,
                'Industry': 'Technology',
                'Stage': 'Proposal',
                'CloseDate': '2025-03-15',
                'CreatedDate': '2025-01-15',
                'DealSizeCategory': 'Medium',
                'LeadSource': 'Website',
                'Type': 'New Business',
                'Probability': 75
            }
        
        # Form fields
        with st.form("opportunity_form"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                opportunity_id = st.text_input("Opportunity ID", value=selected_opp['Id'], key="opp_id")
                amount = st.number_input("Amount ($)", min_value=0, value=selected_opp['Amount'], step=1000, key="amount")
                industry = st.selectbox("Industry", 
                    ["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Education", "Other"], 
                    index=["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Education", "Other"].index(selected_opp['Industry']),
                    key="industry")
                stage = st.selectbox("Stage", 
                    ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"], 
                    index=["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"].index(selected_opp['Stage']),
                    key="stage")
            
            with col_b:
                close_date = st.date_input("Close Date", value=pd.to_datetime(selected_opp['CloseDate']), key="close_date")
                created_date = st.date_input("Created Date", value=pd.to_datetime(selected_opp['CreatedDate']), key="created_date")
                deal_size = st.selectbox("Deal Size", 
                    ["Small", "Medium", "Large"], 
                    index=["Small", "Medium", "Large"].index(selected_opp['DealSizeCategory']),
                    key="deal_size")
                lead_source = st.selectbox("Lead Source", 
                    ["Website", "Referral", "Cold Call", "Trade Show", "Social Media", "Other"], 
                    index=["Website", "Referral", "Cold Call", "Trade Show", "Social Media", "Other"].index(selected_opp['LeadSource']),
                    key="lead_source")
            
            # Additional fields
            opp_type = st.selectbox("Opportunity Type", 
                ["New Business", "Existing Business", "Renewal", "Upsell"], 
                index=["New Business", "Existing Business", "Renewal", "Upsell"].index(selected_opp['Type']),
                key="opp_type")
            probability = st.slider("Probability (%)", 0, 100, selected_opp['Probability'], key="probability")
            
            # Submit button
            submitted = st.form_submit_button("🔍 Analyze Opportunity", use_container_width=True)
    
    with col2:
        st.markdown("### 📊 **Health Analysis Results**")
        
        if submitted and model_loaded:
            # Prepare opportunity data
            opportunity_data = {
                'Id': opportunity_id,
                'Amount': amount,
                'Industry': industry,
                'Stage': stage,
                'CloseDate': close_date.strftime('%Y-%m-%d'),
                'CreatedDate': created_date.strftime('%Y-%m-%d'),
                'DealSizeCategory': deal_size,
                'LeadSource': lead_source,
                'Type': opp_type,
                'Probability': probability
            }
            
            # Show loading state
            with st.spinner("Analyzing opportunity..."):
                try:
                    # Get prediction
                    result = model_service.predict_health_score(opportunity_data)
                    
                    # Display health score gauge
                    fig = create_health_score_gauge(result['health_score'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display results
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        st.metric("Health Score", f"{result['health_score']}/100")
                        st.metric("Risk Level", result['risk_level'])
                    
                    with col_result2:
                        if result.get('confidence'):
                            st.metric("Confidence", f"{result['confidence']:.1%}")
                        
                        # Show model breakdown if available
                        if 'model_predictions' in result and result['model_predictions']:
                            st.markdown("**Model Breakdown:**")
                            predictions = result['model_predictions']
                            if 'ensemble' in predictions:
                                st.write(f"• **Ensemble: {predictions['ensemble']:.1%}**")
                            if 'xgb' in predictions:
                                st.write(f"• XGBoost: {predictions['xgb']:.1%}")
                            if 'lightgbm' in predictions:
                                st.write(f"• LightGBM: {predictions['lightgbm']:.1%}")
                    
                    # Show insights
                    st.markdown("### 💡 **AI Insights**")
                    insights = generate_insights(opportunity_data, result)
                    st.markdown(insights)
                    
                    # Show recommendations
                    st.markdown("### 🎯 **Recommendations**")
                    recommendations = generate_recommendations(opportunity_data, result)
                    st.markdown(recommendations)
                    
                    # Show demo mode indicator
                    if result.get('is_mock_prediction'):
                        st.markdown(create_info_message("🔧 This is a demo prediction using mock data"), unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(create_error_message(f"Error analyzing opportunity: {str(e)}"), unsafe_allow_html=True)
                    st.markdown(create_info_message("💡 **Tip**: Try adjusting the opportunity details or refresh the page"), unsafe_allow_html=True)
        
        elif not model_loaded:
            st.markdown(create_error_message("Model service is not available"), unsafe_allow_html=True)
            st.markdown(create_info_message("Please check the model configuration and try again"), unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #64748b;">
                <h3>Ready to Analyze</h3>
                <p>Fill in the opportunity details on the left and click "Analyze Opportunity" to get started.</p>
            </div>
            """, unsafe_allow_html=True)

def generate_insights(opportunity_data, result):
    """Generate AI-powered insights based on the analysis"""
    health_score = result['health_score']
    risk_level = result['risk_level']
    
    insights = []
    
    # Health score insights
    if health_score >= 80:
        insights.append("✅ **Strong Opportunity**: This deal shows excellent health indicators and high win probability.")
    elif health_score >= 60:
        insights.append("⚠️ **Moderate Risk**: While generally healthy, this opportunity has some areas for improvement.")
    else:
        insights.append("🚨 **High Risk**: This opportunity requires immediate attention to improve win probability.")
    
    # Stage-specific insights
    stage = opportunity_data['Stage']
    if stage == "Prospecting" and health_score < 50:
        insights.append("💡 **Early Stage Focus**: Consider strengthening the initial qualification process.")
    elif stage == "Proposal" and health_score < 70:
        insights.append("📋 **Proposal Enhancement**: Review and strengthen the proposal to increase win probability.")
    elif stage == "Negotiation" and health_score < 80:
        insights.append("🤝 **Negotiation Strategy**: Focus on value proposition and competitive positioning.")
    
    # Amount-based insights
    amount = opportunity_data['Amount']
    if amount > 100000 and health_score < 70:
        insights.append("💰 **High-Value Deal**: This large opportunity requires additional attention to secure.")
    
    # Industry insights
    industry = opportunity_data['Industry']
    if industry == "Technology" and health_score < 75:
        insights.append("🔧 **Tech Sector**: Consider technical requirements and solution alignment.")
    
    return "\n\n".join(insights)

def generate_recommendations(opportunity_data, result):
    """Generate actionable recommendations"""
    health_score = result['health_score']
    recommendations = []
    
    # General recommendations based on health score
    if health_score < 50:
        recommendations.extend([
            "🚨 **Immediate Actions Required:**",
            "• Schedule a detailed opportunity review meeting",
            "• Identify and address key risk factors",
            "• Consider adjusting the sales strategy",
            "• Engage senior management for support"
        ])
    elif health_score < 70:
        recommendations.extend([
            "⚠️ **Improvement Opportunities:**",
            "• Strengthen the value proposition",
            "• Address any customer concerns",
            "• Enhance stakeholder engagement",
            "• Review competitive positioning"
        ])
    else:
        recommendations.extend([
            "✅ **Maintain Momentum:**",
            "• Continue current successful strategies",
            "• Monitor for any changes in customer behavior",
            "• Prepare for successful close",
            "• Document best practices for future deals"
        ])
    
    # Stage-specific recommendations
    stage = opportunity_data['Stage']
    if stage == "Prospecting":
        recommendations.append("\n📋 **Prospecting Best Practices:**")
        recommendations.append("• Ensure proper qualification criteria are met")
        recommendations.append("• Build strong initial relationships")
        recommendations.append("• Understand customer pain points")
    
    elif stage == "Proposal":
        recommendations.append("\n📄 **Proposal Enhancement:**")
        recommendations.append("• Ensure proposal addresses all requirements")
        recommendations.append("• Include clear value proposition")
        recommendations.append("• Provide competitive differentiation")
    
    elif stage == "Negotiation":
        recommendations.append("\n🤝 **Negotiation Strategy:**")
        recommendations.append("• Focus on value over price")
        recommendations.append("• Address any objections proactively")
        recommendations.append("• Maintain strong stakeholder relationships")
    
    return "\n".join(recommendations)

if __name__ == "__main__":
    main()