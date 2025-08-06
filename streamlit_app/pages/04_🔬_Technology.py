"""
🔬 Technology: Advanced ML Architecture & AI Integration
Premium 3D design showcasing the sophisticated technology stack
"""

import streamlit as st
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Add the utils directory to the path
sys.path.append(str(Path(__file__).parent.parent / "utils"))
sys.path.append(str(Path(__file__).parent.parent / "components"))
sys.path.append(str(Path(__file__).parent.parent / "styles"))

# Import our custom modules
from athena_models import get_model_service, get_model_service_status
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
    page_title="Technology - Athena",
    page_icon="🔬",
    layout="wide"
)

def create_model_architecture_chart():
    """Create a premium model architecture visualization"""
    fig = go.Figure()
    
    # Define architecture components
    components = [
        {"name": "Input Features", "x": 0, "y": 0, "color": "#667eea"},
        {"name": "Feature Engineering", "x": 1, "y": 0, "color": "#10b981"},
        {"name": "XGBoost Model", "x": 2, "y": 1, "color": "#f59e0b"},
        {"name": "LightGBM Model", "x": 2, "y": -1, "color": "#ef4444"},
        {"name": "Ensemble Voting", "x": 3, "y": 0, "color": "#8b5cf6"},
        {"name": "Health Score", "x": 4, "y": 0, "color": "#06b6d4"}
    ]
    
    # Add nodes
    for comp in components:
        fig.add_trace(go.Scatter(
            x=[comp["x"]],
            y=[comp["y"]],
            mode='markers+text',
            marker=dict(
                size=30,
                color=comp["color"],
                line=dict(width=2, color='white')
            ),
            text=comp["name"],
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            showlegend=False
        ))
    
    # Add connections
    connections = [
        (0, 1), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5)
    ]
    
    for start, end in connections:
        fig.add_trace(go.Scatter(
            x=[components[start]["x"], components[end]["x"]],
            y=[components[start]["y"], components[end]["y"]],
            mode='lines',
            line=dict(color='#667eea', width=3),
            showlegend=False
        ))
    
    fig.update_layout(
        title="Ensemble Model Architecture",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_size=18,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_performance_metrics_chart():
    """Create a premium performance metrics visualization"""
    metrics = {
        'AUC Score': 0.70,
        'Precision': 0.75,
        'Recall': 0.68,
        'F1 Score': 0.71,
        'Accuracy': 0.73
    }
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=list(metrics.keys()),
        y=list(metrics.values()),
        marker_color='#667eea',
        opacity=0.8,
        hovertemplate="Metric: %{x}<br>Score: %{y:.2f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Model Performance Metrics",
        xaxis_title="Metrics",
        yaxis_title="Score",
        yaxis=dict(range=[0, 1]),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff'),
        title_font_size=18,
        showlegend=False
    )
    
    return fig

def main():
    # Add floating particles background
    st.markdown(add_floating_particles(), unsafe_allow_html=True)
    
    # Premium Header
    st.markdown('<h1 class="main-header">🔬 Technology Stack</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced Machine Learning Architecture & AI Integration</p>', unsafe_allow_html=True)
    
    # Premium Technology Overview
    st.markdown("## 🏗️ **Advanced Architecture**")
    
    # Model Architecture Chart
    arch_fig = create_model_architecture_chart()
    st.plotly_chart(arch_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Premium Performance Metrics
    st.markdown("## 📊 **Model Performance**")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric1 = create_metric_card_3d("AUC Score", "0.70", "+0.05")
        st.markdown(metric1, unsafe_allow_html=True)
    
    with col2:
        metric2 = create_metric_card_3d("Precision", "0.75", "+0.08")
        st.markdown(metric2, unsafe_allow_html=True)
    
    with col3:
        metric3 = create_metric_card_3d("Recall", "0.68", "+0.06")
        st.markdown(metric3, unsafe_allow_html=True)
    
    with col4:
        metric4 = create_metric_card_3d("F1 Score", "0.71", "+0.07")
        st.markdown(metric4, unsafe_allow_html=True)
    
    # Performance Chart
    perf_fig = create_performance_metrics_chart()
    st.plotly_chart(perf_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Premium Technology Stack
    st.markdown("## 🛠️ **Technology Components**")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        # Machine Learning Stack
        ml_card = create_feature_card_3d(
            "🤖 Machine Learning",
            "Advanced ensemble models combining XGBoost and LightGBM with hyperparameter optimization using Optuna. Features 48+ engineered features for comprehensive opportunity analysis.",
            "🤖"
        )
        st.markdown(ml_card, unsafe_allow_html=True)
        
        # AI Integration
        ai_card = create_feature_card_3d(
            "🧠 AI Integration",
            "Google Gemini API integration for natural language insights and diagnostic analysis. Real-time AI-powered recommendations and opportunity health explanations.",
            "🧠"
        )
        st.markdown(ai_card, unsafe_allow_html=True)
        
        # Data Processing
        data_card = create_feature_card_3d(
            "📊 Data Processing",
            "Sophisticated feature engineering pipeline with 48+ engineered features including temporal, categorical, and numerical transformations for optimal model performance.",
            "📊"
        )
        st.markdown(data_card, unsafe_allow_html=True)
    
    with tech_col2:
        # Web Framework
        web_card = create_feature_card_3d(
            "🌐 Web Framework",
            "Streamlit-based interactive web application with premium 3D animations and responsive design. Real-time data visualization and user interactions.",
            "🌐"
        )
        st.markdown(web_card, unsafe_allow_html=True)
        
        # Authentication
        auth_card = create_feature_card_3d(
            "🔐 Authentication",
            "Supabase integration for secure user authentication and database management. Role-based access control and user session management.",
            "🔐"
        )
        st.markdown(auth_card, unsafe_allow_html=True)
        
        # Integration
        integration_card = create_feature_card_3d(
            "🔗 CRM Integration",
            "Salesforce integration with automated workflows and Slack notifications. Real-time opportunity monitoring and automated rescue strategies.",
            "🔗"
        )
        st.markdown(integration_card, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Premium Technical Details
    st.markdown("## 🔧 **Technical Specifications**")
    
    spec_col1, spec_col2 = st.columns(2)
    
    with spec_col1:
        st.markdown("""
        ### 📈 **Model Architecture**
        
        **Ensemble Approach:**
        - **XGBoost**: Gradient boosting with tree-based learning
        - **LightGBM**: Light gradient boosting machine
        - **Voting Classifier**: Weighted ensemble combination
        - **Hyperparameter Optimization**: Optuna for automated tuning
        
        **Feature Engineering:**
        - **48+ Engineered Features**: Temporal, categorical, numerical
        - **Advanced Preprocessing**: Scaling, encoding, normalization
        - **Feature Selection**: Importance-based feature selection
        - **Cross-Validation**: 5-fold stratified cross-validation
        
        **Performance Metrics:**
        - **AUC Score**: 0.70 (70% accuracy)
        - **Precision**: 0.75 (75% precision)
        - **Recall**: 0.68 (68% recall)
        - **F1 Score**: 0.71 (71% F1 score)
        """)
    
    with spec_col2:
        st.markdown("""
        ### 🚀 **System Architecture**
        
        **Frontend:**
        - **Streamlit**: Interactive web application
        - **Plotly**: Advanced data visualizations
        - **CSS3**: Premium 3D animations and effects
        - **Responsive Design**: Mobile and desktop optimized
        
        **Backend:**
        - **Python 3.13**: Modern Python runtime
        - **Scikit-learn**: Machine learning framework
        - **XGBoost**: Gradient boosting library
        - **LightGBM**: Light gradient boosting
        
        **Integration:**
        - **Supabase**: Authentication and database
        - **Salesforce**: CRM integration
        - **Slack**: Notification system
        - **Google Gemini**: AI insights
        """)
    
    st.markdown("---")
    
    # Premium Development Process
    st.markdown("## 🎯 **Development Process**")
    
    process_col1, process_col2 = st.columns(2)
    
    with process_col1:
        st.markdown("""
        ### 🔬 **Research & Design**
        
        1. **Problem Analysis**: Identified sales pipeline health monitoring needs
        2. **Data Collection**: Gathered comprehensive sales opportunity datasets
        3. **Feature Engineering**: Developed 48+ engineered features
        4. **Model Selection**: Evaluated multiple ML algorithms
        
        ### 🤖 **Machine Learning**
        
        1. **Data Preprocessing**: Comprehensive data cleaning and preparation
        2. **Model Training**: Ensemble approach with XGBoost and LightGBM
        3. **Hyperparameter Tuning**: Automated optimization with Optuna
        4. **Performance Evaluation**: Cross-validation and metrics analysis
        """)
    
    with process_col2:
        st.markdown("""
        ### 🌐 **Web Development**
        
        1. **UI/UX Design**: Premium dark theme with 3D animations
        2. **Frontend Development**: Streamlit-based interactive application
        3. **Data Visualization**: Advanced charts and analytics dashboard
        4. **User Experience**: Intuitive navigation and responsive design
        
        ### 🔗 **Integration & Deployment**
        
        1. **API Development**: RESTful API for model serving
        2. **Authentication**: Supabase integration for user management
        3. **CRM Integration**: Salesforce and Slack automation
        4. **Deployment**: Production-ready application architecture
        """)
    
    # Premium Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #71717a; font-size: 0.875rem; padding: 1rem;">
        Built with cutting-edge technology | Powered by AI & ML
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()