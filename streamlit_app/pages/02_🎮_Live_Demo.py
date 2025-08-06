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
from athena_styles import load_advanced_css
from animations import create_progress_ring, create_success_animation, add_hover_effects

# Configure the page
st.set_page_config(
    page_title="Athena - Live Demo",
    page_icon="🎮",
    layout="wide"
)

# Load advanced CSS with animations
load_advanced_css()
add_hover_effects()

def main():
    st.markdown('<h1 class="demo-header">🎮 Live Opportunity Health Checker</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: #666;">
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
                st.warning("🔧 **Demo Mode**: Using mock predictions (real models unavailable)")
                st.info("💡 **Demo continues**: You can still test the interface and see realistic predictions")
                model_loaded = True
            else:
                st.error(f"❌ **Model Error**: {service_status['error']}")
                model_loaded = False
        else:
            model_loaded = True
            if service_status.get('is_mock'):
                st.info("🔧 Running in demo mode with mock predictions")
                
    except Exception as e:
        st.error(f"❌ **Unexpected Error**: {str(e)}")
        st.info("💡 **Troubleshooting**: Please check that model files are in the correct location")
        model_loaded = False
    
    # Main layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
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
            selected_sample = sample_opportunities[idx]
        else:
            selected_sample = {
                'Id': 'CUSTOM001',
                'Amount': 250000,
                'StageName': 'Proposal',
                'Industry': 'Technology',
                'Region': 'North America',
                'DaysInStage': 30,
                'EmailOpens': 25,
                'EmailClicks': 8,
                'ContentDownloads': 3,
                'MeetingsScheduled': 4,
                'CallsMade': 12,
                'SupportCases': 0,
                'CriticalCases': 0,
                'AvgCaseAge': 0,
                'CloseDatePushed': 0,
                'LastActivityDays': 7,
                'CommunicationFrequency': 10
            }
        
        st.markdown("---")
        
        # Input form
        with st.form("opportunity_form"):
            # Basic Opportunity Info
            st.markdown("**🎯 Basic Information**")
            col_a, col_b = st.columns(2)
            
            with col_a:
                opp_id = st.text_input("Opportunity ID", value=selected_sample['Id'])
                amount = st.number_input("Deal Amount ($)", min_value=1000, max_value=10000000, 
                                       value=selected_sample['Amount'], step=10000)
                industry = st.selectbox("Industry", 
                                      ["Technology", "Healthcare", "Financial Services", "Manufacturing", 
                                       "Retail", "Education", "Government", "Other"],
                                      index=["Technology", "Healthcare", "Financial Services", "Manufacturing", 
                                           "Retail", "Education", "Government", "Other"].index(selected_sample['Industry']))
            
            with col_b:
                stage = st.selectbox("Sales Stage",
                                   ["Prospecting", "Qualification", "Needs Analysis", "Value Proposition", 
                                    "Proposal", "Negotiation", "Closed Won", "Closed Lost"],
                                   index=["Prospecting", "Qualification", "Needs Analysis", "Value Proposition", 
                                        "Proposal", "Negotiation", "Closed Won", "Closed Lost"].index(selected_sample['StageName']))
                region = st.selectbox("Region", 
                                     ["North America", "Europe", "Asia Pacific", "Latin America", "Other"],
                                     index=["North America", "Europe", "Asia Pacific", "Latin America", "Other"].index(selected_sample['Region']))
                days_in_stage = st.slider("Days in Current Stage", 0, 180, selected_sample['DaysInStage'])
            
            # Marketing Engagement
            st.markdown("**📧 Marketing Engagement**")
            col_c, col_d, col_e = st.columns(3)
            
            with col_c:
                email_opens = st.number_input("Email Opens", min_value=0, max_value=200, 
                                            value=selected_sample['EmailOpens'])
                email_clicks = st.number_input("Email Clicks", min_value=0, max_value=100, 
                                             value=selected_sample['EmailClicks'])
            
            with col_d:
                content_downloads = st.number_input("Content Downloads", min_value=0, max_value=50, 
                                                  value=selected_sample['ContentDownloads'])
                meetings_scheduled = st.number_input("Meetings Scheduled", min_value=0, max_value=50, 
                                                   value=selected_sample['MeetingsScheduled'])
            
            with col_e:
                calls_made = st.number_input("Calls Made", min_value=0, max_value=100, 
                                           value=selected_sample['CallsMade'])
                comm_frequency = st.number_input("Communication Frequency (per week)", min_value=0, max_value=20, 
                                               value=selected_sample['CommunicationFrequency'])
            
            # Support & Risk Indicators
            st.markdown("**🛠️ Support & Risk Indicators**")
            col_f, col_g = st.columns(2)
            
            with col_f:
                support_cases = st.number_input("Support Cases", min_value=0, max_value=20, 
                                              value=selected_sample['SupportCases'])
                critical_cases = st.number_input("Critical Support Cases", min_value=0, max_value=10, 
                                                value=selected_sample['CriticalCases'])
                avg_case_age = st.number_input("Average Case Age (days)", min_value=0, max_value=90, 
                                             value=selected_sample['AvgCaseAge'])
            
            with col_g:
                close_date_pushed = st.number_input("Close Date Pushbacks", min_value=0, max_value=10, 
                                                  value=selected_sample['CloseDatePushed'])
                last_activity_days = st.number_input("Days Since Last Activity", min_value=0, max_value=90, 
                                                   value=selected_sample['LastActivityDays'])
            
            # Submit button
            submitted = st.form_submit_button("🔍 **Analyze Opportunity Health**", 
                                            use_container_width=True, type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if submitted and model_loaded:
            # Prepare opportunity data
            opportunity_data = {
                'Id': opp_id,
                'Amount': amount,
                'StageName': stage,
                'Industry': industry,
                'Region': region,
                'DaysInStage': days_in_stage,
                'EmailOpens': email_opens,
                'EmailClicks': email_clicks,
                'ContentDownloads': content_downloads,
                'MeetingsScheduled': meetings_scheduled,
                'CallsMade': calls_made,
                'SupportCases': support_cases,
                'CriticalCases': critical_cases,
                'AvgCaseAge': avg_case_age,
                'CloseDatePushed': close_date_pushed,
                'LastActivityDays': last_activity_days,
                'CommunicationFrequency': comm_frequency
            }
            
            with st.spinner("🤖 Analyzing opportunity with AI..."):
                try:
                    # Validate inputs before prediction
                    if amount <= 0:
                        st.error("❌ **Invalid Input**: Deal amount must be greater than $0")
                        st.stop()
                    
                    if days_in_stage < 0:
                        st.error("❌ **Invalid Input**: Days in stage cannot be negative")
                        st.stop()
                    
                    # Get prediction with enhanced error handling
                    result = model_service.predict_health_score(opportunity_data)
                    
                    # Show warnings if using mock predictions
                    if result.get('is_mock_prediction'):
                        st.warning("🔧 **Demo Mode**: Showing mock predictions for demonstration")
                    
                    if result.get('prediction_warnings'):
                        for warning in result['prediction_warnings']:
                            st.warning(f"⚠️ {warning}")
                    
                    # Success animation
                    success_anim = create_success_animation("Analysis Complete!")
                    st.markdown(success_anim, unsafe_allow_html=True)
                    
                    # Display health score gauge
                    fig = create_health_score_gauge(result['health_score'], result['risk_level'])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Animated progress ring for health score
                    progress_ring = create_progress_ring(result['health_score'])
                    st.markdown(progress_ring, unsafe_allow_html=True)
                    
                    # Results section
                    st.markdown('<div class="result-section floating">', unsafe_allow_html=True)
                    st.markdown(f"### 🎯 **Health Analysis Results**")
                    
                    col_x, col_y = st.columns(2)
                    with col_x:
                        st.metric("Health Score", f"{result['health_score']}/100", 
                                delta=f"{result['health_score'] - 50:+d} from average")
                    with col_y:
                        st.metric("Win Probability", f"{result['probability']:.1%}",
                                delta=f"{result['probability'] - 0.5:+.1%} from baseline")
                    
                    # Risk level with appropriate styling
                    risk_class = f"risk-{result['risk_level'].lower().replace(' ', '-')}"
                    st.markdown(f'<div class="metric-card {risk_class}"><h4>Risk Level: {result["risk_level"]}</h4></div>', 
                              unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Model breakdown
                    if 'model_predictions' in result and result['model_predictions']:
                        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                        st.markdown("### 🔬 **Model Breakdown**")
                        predictions = result['model_predictions']
                        
                        # Show which models were used
                        if result.get('models_used'):
                            st.caption(f"**Models used**: {', '.join(result['models_used'])}")
                        
                        if 'ensemble' in predictions:
                            st.progress(predictions['ensemble'], text=f"Ensemble Model: {predictions['ensemble']:.1%}")
                        if 'xgb' in predictions:
                            st.progress(predictions['xgb'], text=f"XGBoost: {predictions['xgb']:.1%}")
                        if 'lightgbm' in predictions:
                            st.progress(predictions['lightgbm'], text=f"LightGBM: {predictions['lightgbm']:.1%}")
                        if 'mock' in predictions:
                            st.progress(predictions['mock'], text=f"Demo Model: {predictions['mock']:.1%}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # AI-Powered Insights
                    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                    st.markdown("### 🧠 **AI-Powered Insights**")
                    
                    # Generate insights based on the data
                    insights = generate_insights(opportunity_data, result)
                    for insight in insights:
                        st.markdown(f"• {insight}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Recommendations
                    st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                    st.markdown("### 💡 **Recommended Actions**")
                    
                    recommendations = generate_recommendations(opportunity_data, result)
                    for i, rec in enumerate(recommendations, 1):
                        st.markdown(f"**{i}.** {rec}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Export functionality
                    st.markdown("---")
                    st.markdown("### 📊 **Export Report**")
                    
                    col_export1, col_export2, col_export3 = st.columns(3)
                    
                    with col_export1:
                        if st.button("📄 Export PDF Report", key="export_pdf"):
                            st.info("📄 Generating PDF report...")
                            # Simulate PDF generation
                            import time
                            with st.spinner("Creating PDF..."):
                                time.sleep(2)
                            st.success("✅ PDF report generated! (Demo mode)")
                    
                    with col_export2:
                        if st.button("📊 Export Data", key="export_data"):
                            st.info("📊 Preparing data export...")
                            # Create downloadable data
                            import pandas as pd
                            export_data = pd.DataFrame([{
                                'Opportunity ID': opportunity_data['Id'],
                                'Health Score': result['health_score'],
                                'Risk Level': result['risk_level'],
                                'Probability': f"{result['probability']:.1%}",
                                'Amount': f"${opportunity_data['Amount']:,}",
                                'Stage': opportunity_data['StageName'],
                                'Industry': opportunity_data['Industry'],
                                'Analysis Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                            }])
                            st.download_button(
                                label="⬇️ Download CSV",
                                data=export_data.to_csv(index=False),
                                file_name=f"athena_analysis_{opportunity_data['Id']}.csv",
                                mime="text/csv"
                            )
                    
                    with col_export3:
                        if st.button("📈 Export Chart", key="export_chart"):
                            st.info("📈 Preparing chart export...")
                            # Export the health score gauge as image
                            import plotly.io as pio
                            pio.kaleido.scope.default_format = "png"
                            pio.kaleido.scope.default_width = 800
                            pio.kaleido.scope.default_height = 600
                            
                            # Convert chart to image
                            img_bytes = fig.to_image(format="png")
                            st.download_button(
                                label="🖼️ Download Chart",
                                data=img_bytes,
                                file_name=f"athena_health_score_{opportunity_data['Id']}.png",
                                mime="image/png"
                            )
                    
                except DataValidationError as e:
                    st.error(f"❌ **Input Validation Error**: {str(e)}")
                    st.info("💡 **Tip**: Please check your input values and try again")
                except PredictionError as e:
                    st.error(f"❌ **Prediction Error**: {str(e)}")
                    st.info("💡 **Tip**: The model may be having issues. Try refreshing the page")
                except AthenaModelError as e:
                    st.error(f"❌ **Model Error**: {str(e)}")
                    st.info("💡 **Tip**: Please contact support if this persists")
                except Exception as e:
                    st.error(f"❌ **Unexpected Error**: {str(e)}")
                    st.info("💡 **Tip**: Please try again or refresh the page")
                    # Only show full traceback in debug mode
                    if st.secrets.get("debug_mode", False):
                        st.exception(e)
        
        elif not model_loaded:
            st.warning("🔧 **Model Service Unavailable**")
            st.info("Please ensure the Athena models are properly trained and loaded.")
        
        else:
            st.info("👆 **Fill out the form and click 'Analyze' to see results**")
            
            # Show sample results for demo
            st.markdown("### 📊 **Sample Analysis**")
            st.markdown("*This is what you'll see after analyzing an opportunity:*")
            
            # Create sample gauge
            sample_fig = create_health_score_gauge(73, "Medium Risk")
            st.plotly_chart(sample_fig, use_container_width=True)
            
            st.info("""
            **Sample insights:**
            • High engagement with marketing content
            • Deal velocity within industry average
            • Recommended: Schedule follow-up meeting
            """)

def generate_insights(opportunity_data, result):
    """Generate AI-powered insights based on opportunity data"""
    insights = []
    
    # Engagement analysis
    engagement_score = (opportunity_data['EmailOpens'] * 0.3 + 
                       opportunity_data['EmailClicks'] * 0.7 + 
                       opportunity_data['ContentDownloads'] * 1.5)
    
    if engagement_score > 20:
        insights.append("🟢 **High engagement** with marketing content indicates strong interest")
    elif engagement_score > 10:
        insights.append("🟡 **Moderate engagement** - opportunity for increased touchpoints")
    else:
        insights.append("🔴 **Low engagement** - requires immediate attention and re-engagement")
    
    # Deal velocity analysis
    deal_velocity = opportunity_data['Amount'] / (opportunity_data['DaysInStage'] + 1)
    if deal_velocity > 5000:
        insights.append("⚡ **Deal velocity is strong** - progressing well through pipeline")
    else:
        insights.append("🐌 **Deal velocity is slow** - may indicate stalled progress")
    
    # Risk indicators
    if opportunity_data['LastActivityDays'] > 14:
        insights.append("⚠️ **Communication gap detected** - no recent activity")
    
    if opportunity_data['CriticalCases'] > 0:
        insights.append("🚨 **Critical support issues** may impact deal progression")
    
    if opportunity_data['CloseDatePushed'] > 1:
        insights.append("📅 **Multiple close date pushbacks** suggest timing or readiness issues")
    
    # Stage analysis
    if opportunity_data['DaysInStage'] > 60:
        insights.append("⏰ **Extended time in stage** - may need intervention to advance")
    
    return insights

def generate_recommendations(opportunity_data, result):
    """Generate actionable recommendations"""
    recommendations = []
    
    health_score = result['health_score']
    
    if health_score < 40:
        recommendations.append("🚨 **Immediate intervention required** - Schedule executive review meeting")
        recommendations.append("📞 **Escalate to senior sales leader** for relationship rebuild")
    elif health_score < 60:
        recommendations.append("📅 **Schedule urgent follow-up meeting** within 48 hours")
        recommendations.append("🎯 **Re-engage with value proposition** tailored to current needs")
    elif health_score < 80:
        recommendations.append("📈 **Accelerate deal progression** with next-step planning")
        recommendations.append("🤝 **Introduce technical/implementation team** for deeper engagement")
    else:
        recommendations.append("🎉 **Deal is on track** - maintain momentum with regular check-ins")
        recommendations.append("📋 **Prepare for contract negotiation** and legal review")
    
    # Specific recommendations based on data
    if opportunity_data['LastActivityDays'] > 14:
        recommendations.append("📧 **Re-establish communication** - send personalized follow-up")
    
    if opportunity_data['EmailOpens'] < 10:
        recommendations.append("📬 **Improve email engagement** with more relevant content")
    
    if opportunity_data['MeetingsScheduled'] < 3:
        recommendations.append("🗓️ **Increase face time** - schedule more meetings and demos")
    
    if opportunity_data['CriticalCases'] > 0:
        recommendations.append("🛠️ **Resolve support issues** before advancing deal")
    
    return recommendations[:4]  # Limit to top 4 recommendations

if __name__ == "__main__":
    main()