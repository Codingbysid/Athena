"""
🔬 Technology - Advanced ML & AI Architecture
Technical deep-dive into Athena's AI-powered sales intelligence
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import json

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import get_model_service
from athena_styles import load_advanced_css

# Configure the page
st.set_page_config(
    page_title="Athena - Technology",
    page_icon="🔬",
    layout="wide"
)

# Load advanced CSS with animations
load_advanced_css()

def main():
    st.markdown('<h1 class="tech-header">🔬 Advanced Technology Stack</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; margin: 1rem 0; color: #666;">
        Deep dive into Athena's cutting-edge ML architecture and AI-powered capabilities
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize model service
    try:
        model_service = get_model_service()
        model_info = model_service.get_model_info()
        model_loaded = True
    except Exception as e:
        st.warning(f"⚠️ Model service unavailable: {str(e)}")
        model_loaded = False
        model_info = None
    
    # Model Architecture Section
    st.markdown("## 🤖 **Machine Learning Architecture**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="model-card">
            <h3>🌲 XGBoost</h3>
            <p>Gradient Boosting</p>
            <h4>AUC: 0.6969</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="model-card">
            <h3>🚀 LightGBM</h3>
            <p>Gradient Boosting</p>
            <h4>AUC: 0.6946</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="model-card">
            <h3>🎯 Ensemble</h3>
            <p>Voting Classifier</p>
            <h4>AUC: 0.6968</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance Metrics
    st.markdown("### 📈 **Model Performance Metrics**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="performance-metric">
            <h3>70%</h3>
            <p>AUC Score</p>
            <small>Ensemble Model</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="performance-metric">
            <h3>48</h3>
            <p>Features</p>
            <small>Engineered</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="performance-metric">
            <h3>±0.05</h3>
            <p>CV Stability</p>
            <small>Cross-validation</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="performance-metric">
            <h3>< 100ms</h3>
            <p>Prediction Time</p>
            <small>Real-time</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Architecture Diagram
    st.markdown("## 🏗️ **System Architecture**")
    
    st.markdown('<div class="architecture-box">', unsafe_allow_html=True)
    
    # Create architecture diagram using text
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────┐
    │                        ATHENA ARCHITECTURE                      │
    └─────────────────────────────────────────────────────────────────┘
    
    📊 DATA SOURCES                    🤖 ML PIPELINE                  🌐 DEPLOYMENT
    ├── Salesforce CRM                 ├── Feature Engineering         ├── Streamlit Web App
    ├── Marketing Automation           ├── Data Preprocessing          ├── Flask API Service
    ├── Support Systems                ├── Model Training             ├── Real-time Monitoring
    └── Activity Tracking              └── Ensemble Prediction        └── Analytics Dashboard
                   │                              │                              │
                   └──────────────────────────────┼──────────────────────────────┘
                                                  │
    🔄 REAL-TIME PROCESSING            ┌─────────────────────────┐
    ├── Health Score Calculation       │    ENSEMBLE MODELS     │
    ├── Risk Assessment               │  ┌─────────┬─────────┐  │
    ├── AI Diagnostics                │  │ XGBoost │ LightGBM│  │
    └── Automated Workflows           │  └─────────┴─────────┘  │
                                     │   Voting Classifier    │
                                     └─────────────────────────┘
    ```
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feature Engineering
    st.markdown("## ⚙️ **Advanced Feature Engineering**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tech-section">', unsafe_allow_html=True)
        st.markdown("### 🔧 **Engineered Features**")
        st.markdown("""
        **Engagement Metrics:**
        - TotalEmailEngagement = EmailOpens + EmailClicks
        - EngagementScore = EmailOpens×0.3 + EmailClicks×0.7 + Downloads×1.5
        - CommunicationGap = Days since last activity
        
        **Deal Velocity:**
        - DealVelocity = Amount / (DaysInStage + 1)
        - StageProgress = Current stage order / Total stages
        - IsStalled = DaysInStage > 60 days
        
        **Risk Indicators:**
        - HasCriticalIssues = CriticalCases > 0
        - IsOverdue = LastActivity > 14 days
        - RiskScore = Weighted risk factors
        
        **Industry Intelligence:**
        - IndustryWinRate = Historical win rates by industry
        - DealSizeCategory = Binned deal sizes
        - RegionalFactors = Geographic performance
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="tech-section">', unsafe_allow_html=True)
        st.markdown("### 📊 **Data Pipeline**")
        st.markdown("""
        **1. Data Ingestion**
        ```python
        # Real-time data collection
        salesforce_data = get_opportunity_data()
        marketing_data = get_engagement_metrics()
        support_data = get_case_information()
        ```
        
        **2. Feature Engineering**
        ```python
        # Advanced feature creation
        df['DealVelocity'] = df['Amount'] / (df['DaysInStage'] + 1)
        df['EngagementScore'] = calculate_engagement(df)
        df['RiskScore'] = assess_risk_factors(df)
        ```
        
        **3. Model Prediction**
        ```python
        # Ensemble prediction
        xgb_pred = xgb_model.predict_proba(X)[0][1]
        lgb_pred = lgb_model.predict_proba(X)[0][1]
        final_score = voting_classifier.predict_proba(X)[0][1]
        ```
        
        **4. Real-time Scoring**
        ```python
        # Health score calculation
        health_score = int(final_score * 100)
        risk_level = classify_risk(health_score)
        ```
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Integration
    st.markdown("## 🧠 **AI-Powered Intelligence**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tech-section">', unsafe_allow_html=True)
        st.markdown("### 🤖 **Google Gemini Integration**")
        st.markdown("""
        **Natural Language Diagnostics:**
        - Contextual opportunity analysis
        - Risk factor explanations
        - Actionable recommendations
        - Deal progression insights
        
        **AI Capabilities:**
        - Pattern recognition across deals
        - Predictive text generation
        - Sentiment analysis of communications
        - Automated report generation
        
        **Integration Points:**
        - Real-time diagnosis API calls
        - Batch processing for reports
        - Custom prompt engineering
        - Response validation and formatting
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="tech-section">', unsafe_allow_html=True)
        st.markdown("### ⚡ **Real-time Monitoring**")
        st.markdown("""
        **Performance Tracking:**
        - Prediction accuracy monitoring
        - Model drift detection
        - A/B testing framework
        - Performance degradation alerts
        
        **System Metrics:**
        - API response times
        - Prediction throughput
        - Error rates and logging
        - Resource utilization
        
        **Business Intelligence:**
        - Win rate improvements
        - Deal velocity changes
        - Intervention success rates
        - ROI measurement
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Model Details
    if model_loaded and model_info:
        st.markdown("## 🔍 **Model Status & Details**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 **Loaded Components**")
            
            # Model status
            models_status = model_info.get('models_loaded', {})
            artifacts_status = model_info.get('artifacts_loaded', {})
            
            st.markdown("**Models:**")
            for model_name, loaded in models_status.items():
                status = "✅" if loaded else "❌"
                st.markdown(f"- {status} {model_name.title()}")
            
            st.markdown("**Artifacts:**")
            for artifact_name, loaded in artifacts_status.items():
                status = "✅" if loaded else "❌"
                st.markdown(f"- {status} {artifact_name.title()}")
        
        with col2:
            st.markdown("### 📊 **Performance Metadata**")
            
            if 'performance' in model_info and model_info['performance']:
                metadata = model_info['performance']
                st.json(metadata)
            else:
                st.info("Performance metadata not available")
    
    # Technology Stack
    st.markdown("## 🛠️ **Technology Stack**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🐍 **Core ML Stack**
        - **Python 3.12+**
        - **Scikit-learn** - ML framework
        - **XGBoost** - Gradient boosting
        - **LightGBM** - Fast boosting
        - **Pandas** - Data manipulation
        - **NumPy** - Numerical computing
        - **Optuna** - Hyperparameter tuning
        """)
    
    with col2:
        st.markdown("""
        ### 🌐 **Web & API**
        - **Streamlit** - Web application
        - **Flask** - API framework
        - **Plotly** - Interactive charts
        - **SQLite** - Tracking database
        - **Requests** - HTTP client
        - **JSON** - Data interchange
        - **RESTful APIs** - Service architecture
        """)
    
    with col3:
        st.markdown("""
        ### ☁️ **Integration & Deployment**
        - **Google Gemini** - AI diagnostics
        - **Salesforce** - CRM integration
        - **Slack** - Notifications
        - **GitHub** - Version control
        - **Docker** - Containerization
        - **Cloud Hosting** - Scalable deployment
        - **Monitoring** - Performance tracking
        """)
    
    # Code Examples
    st.markdown("## 💻 **Code Examples**")
    
    # Prediction example
    st.markdown("### 🎯 **Health Score Prediction**")
    
    st.code("""
# Example: Real-time health score prediction
from athena_models import get_model_service

# Initialize model service
model_service = get_model_service()

# Opportunity data
opportunity = {
    'Amount': 250000,
    'StageName': 'Proposal',
    'Industry': 'Technology',
    'DaysInStage': 30,
    'EmailOpens': 25,
    'EmailClicks': 8,
    'ContentDownloads': 3,
    'MeetingsScheduled': 4,
    'CallsMade': 12,
    'SupportCases': 0,
    'CriticalCases': 0,
    'LastActivityDays': 5
}

# Get prediction
result = model_service.predict_health_score(opportunity)

print(f"Health Score: {result['health_score']}/100")
print(f"Risk Level: {result['risk_level']}")
print(f"Win Probability: {result['probability']:.2%}")
""", language="python")
    
    # Feature engineering example
    st.markdown("### ⚙️ **Feature Engineering**")
    
    st.code("""
# Example: Advanced feature engineering
def engineer_features(df):
    # Deal velocity
    df['DealVelocity'] = df['Amount'] / (df['DaysInStage'] + 1)
    
    # Engagement scoring
    df['EngagementScore'] = (
        df['EmailOpens'] * 0.3 + 
        df['EmailClicks'] * 0.7 + 
        df['ContentDownloads'] * 1.5
    )
    
    # Risk indicators
    df['IsStalled'] = (df['DaysInStage'] > 60).astype(int)
    df['IsOverdue'] = (df['LastActivityDays'] > 14).astype(int)
    df['HasCriticalIssues'] = (df['CriticalCases'] > 0).astype(int)
    
    # Risk score calculation
    df['RiskScore'] = (
        df['IsStalled'] * 0.3 +
        df['IsOverdue'] * 0.2 +
        df['HasCriticalIssues'] * 0.4 +
        (df['CommunicationGap'] / 30) * 0.1
    )
    
    return df
""", language="python")
    
    # Performance metrics
    st.markdown("## 📈 **Performance Improvements**")
    
    improvement_data = {
        'Metric': ['AUC Score', 'Model Stability', 'Feature Count', 'Prediction Speed', 'Business Impact'],
        'Baseline': ['0.6241', '±0.1617', '27', '~200ms', 'Manual analysis'],
        'Enhanced': ['0.6968', '±0.05', '48', '<100ms', 'Automated insights'],
        'Improvement': ['+11.7%', '+70%', '+78%', '+50%', 'Continuous']
    }
    
    st.dataframe(
        pd.DataFrame(improvement_data),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Future Roadmap
    st.markdown("## 🚀 **Future Roadmap**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 **Near-term (Q1 2025)**
        - [ ] **Advanced NLP** - Email sentiment analysis
        - [ ] **Time Series** - Seasonal trend modeling
        - [ ] **Deep Learning** - Neural network ensemble
        - [ ] **Real-time Training** - Continuous model updates
        - [ ] **Multi-modal** - Document and image analysis
        """)
    
    with col2:
        st.markdown("""
        ### 🌟 **Long-term (2025+)**
        - [ ] **Causal AI** - Root cause analysis
        - [ ] **Federated Learning** - Cross-client models
        - [ ] **Explainable AI** - Advanced interpretability
        - [ ] **AutoML** - Automated model optimization
        - [ ] **Edge Computing** - Local inference
        """)

if __name__ == "__main__":
    main()