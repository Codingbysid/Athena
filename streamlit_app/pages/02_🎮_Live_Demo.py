"""
🎮 Live Demo: Interactive Opportunity Health Analysis
Premium 3D design with advanced animations and user interactions
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
    create_loading_3d, add_floating_particles
)

# Load premium CSS with 3D animations
load_advanced_css()

# Page configuration
st.set_page_config(
    page_title="Live Demo - Athena",
    page_icon="🎮",
    layout="wide"
)

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Premium Header
    st.markdown('<h1 class="main-header">🎮 Live Demo</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Experience AI-Powered Sales Intelligence in Action</p>', unsafe_allow_html=True)
    
    # Get model service
    model_service = get_model_service()
    
    # Premium Demo Section
    st.markdown("## 🔍 **Analyze Opportunity Health**")
    
    # Create two columns for input and results
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 **Opportunity Details**")
        
        # Premium form with 3D styling
        with st.container():
            st.markdown("""
            <div style="background: var(--bg-card); border-radius: var(--radius-xl); padding: var(--space-xl); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: var(--shadow-md);">
            """, unsafe_allow_html=True)
            
            # Opportunity Name
            opportunity_name = st.text_input(
                "Opportunity Name",
                value="Enterprise Software Deal",
                help="Enter the name of the opportunity"
            )
            
            # Deal Size
            deal_size = st.number_input(
                "Deal Size ($)",
                min_value=1000,
                max_value=10000000,
                value=500000,
                step=10000,
                help="Enter the total deal value"
            )
            
            # Sales Stage
            sales_stage = st.selectbox(
                "Sales Stage",
                options=["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
                index=2,
                help="Current stage in the sales process"
            )
            
            # Days in Stage
            days_in_stage = st.number_input(
                "Days in Current Stage",
                min_value=1,
                max_value=365,
                value=30,
                help="Number of days in the current stage"
            )
            
            # Lead Source
            lead_source = st.selectbox(
                "Lead Source",
                options=["Website", "Referral", "Cold Call", "Trade Show", "Social Media", "Email Campaign"],
                index=0,
                help="How the lead was acquired"
            )
            
            # Company Size
            company_size = st.selectbox(
                "Company Size",
                options=["1-10", "11-50", "51-200", "201-1000", "1000+"],
                index=2,
                help="Size of the prospect company"
            )
            
            # Industry
            industry = st.selectbox(
                "Industry",
                options=["Technology", "Healthcare", "Finance", "Manufacturing", "Retail", "Education", "Other"],
                index=0,
                help="Industry of the prospect"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Premium Analyze Button
            if st.button("🔍 Analyze Opportunity", key="analyze_button", use_container_width=True):
                st.session_state.analyzing = True
                st.session_state.opportunity_data = {
                    "OpportunityName": opportunity_name,
                    "Amount": deal_size,
                    "StageName": sales_stage,
                    "DaysInStage": days_in_stage,
                    "LeadSource": lead_source,
                    "CompanySize": company_size,
                    "Industry": industry
                }
    
    with col2:
        st.markdown("### 📊 **Analysis Results**")
        
        # Show loading animation while analyzing
        if st.session_state.get('analyzing', False):
            st.markdown(create_loading_3d(), unsafe_allow_html=True)
            st.markdown("**Analyzing opportunity health...**")
            
            # Simulate processing time for better UX
            time.sleep(1.5)
            
            try:
                # Get prediction
                result = model_service.predict_health_score(st.session_state.opportunity_data)
                
                # Clear loading state
                st.session_state.analyzing = False
                st.session_state.result = result
                
                # Rerun to show results
                st.rerun()
                
            except Exception as e:
                st.session_state.analyzing = False
                st.error(f"Error analyzing opportunity: {str(e)}")
        
        # Show results if available
        elif st.session_state.get('result'):
            result = st.session_state.result
            
            # Premium Results Display
            st.markdown("""
            <div style="background: var(--bg-card); border-radius: var(--radius-xl); padding: var(--space-xl); border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: var(--shadow-md);">
            """, unsafe_allow_html=True)
            
            # Health Score
            health_score = result.get('health_score', 0)
            health_percentage = int(health_score * 100)
            
            # Create health score gauge
            gauge_fig = create_health_score_gauge(health_percentage)
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            # Health Status
            if health_percentage >= 80:
                status = "🟢 Excellent"
                status_color = "var(--success)"
            elif health_percentage >= 60:
                status = "🟡 Good"
                status_color = "var(--warning)"
            elif health_percentage >= 40:
                status = "🟠 Fair"
                status_color = "var(--warning)"
            else:
                status = "🔴 Poor"
                status_color = "var(--danger)"
            
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <h3 style="color: {status_color};">{status}</h3>
                <p style="color: var(--text-secondary);">Health Score: {health_percentage}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Insights
            st.markdown("### 💡 **Key Insights**")
            
            insights = result.get('insights', [])
            if insights:
                for insight in insights[:3]:  # Show top 3 insights
                    st.markdown(f"• {insight}")
            else:
                st.markdown("• Opportunity shows moderate health indicators")
                st.markdown("• Consider increasing engagement activities")
                st.markdown("• Monitor progress closely in current stage")
            
            # Recommendations
            st.markdown("### 🎯 **Recommendations**")
            
            recommendations = result.get('recommendations', [])
            if recommendations:
                for rec in recommendations[:3]:  # Show top 3 recommendations
                    st.markdown(f"• {rec}")
            else:
                st.markdown("• Schedule follow-up meetings")
                st.markdown("• Provide additional product demos")
                st.markdown("• Address any outstanding objections")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Success message
            st.markdown(create_success_message_3d("Analysis completed successfully!"), unsafe_allow_html=True)
    
    # Premium Sample Opportunities
    st.markdown("---")
    st.markdown("## 🎲 **Try Sample Opportunities**")
    
    # Get sample opportunities
    sample_opportunities = get_sample_opportunities()
    
    if sample_opportunities:
        # Create columns for sample opportunities
        cols = st.columns(3)
        
        for i, opp in enumerate(sample_opportunities[:3]):  # Show first 3 samples
            with cols[i]:
                opp_name = opp.get('OpportunityName', f'Sample {i+1}')
                opp_amount = opp.get('Amount', 0)
                
                sample_card = create_feature_card_3d(
                    opp_name,
                    f"Deal Size: ${opp_amount:,}",
                    "📋"
                )
                st.markdown(sample_card, unsafe_allow_html=True)
                
                if st.button(f"Analyze {opp_name}", key=f"sample_{i}"):
                    st.session_state.opportunity_data = opp
                    st.session_state.analyzing = True
                    st.rerun()
    
    # Premium Information Section
    st.markdown("---")
    st.markdown("## ℹ️ **How It Works**")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        ### 🤖 **AI Analysis Process**
        
        1. **Feature Engineering**: 48+ features are extracted and engineered
        2. **Ensemble Prediction**: XGBoost + LightGBM models analyze the data
        3. **Health Scoring**: Opportunity receives a 0-100 health score
        4. **AI Insights**: Google Gemini provides natural language analysis
        5. **Recommendations**: Actionable steps to improve opportunity health
        """)
    
    with info_col2:
        st.markdown("""
        ### 📊 **Key Metrics Analyzed**
        
        - **Deal Size & Stage**: Current position in sales cycle
        - **Engagement History**: Past interactions and activities
        - **Company Profile**: Industry, size, and characteristics
        - **Market Factors**: Competition and market conditions
        - **Behavioral Patterns**: Sales team interactions and timing
        """)

if __name__ == "__main__":
    main()