"""
🎨 3D Animation Components for Athena
Inspired by modern corporate websites like Montfort
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, List, Optional

def create_3d_hero_section():
    """Create a 3D hero section with floating elements"""
    return """
    <div class="hero-3d-container">
        <div class="floating-cube cube-1"></div>
        <div class="floating-cube cube-2"></div>
        <div class="floating-cube cube-3"></div>
        <div class="hero-content">
            <h1 class="hero-title">🚀 ATHENA</h1>
            <p class="hero-subtitle">AI-Powered Sales Intelligence Platform</p>
            <div class="hero-description">
                Transform your sales operations with intelligent opportunity health scoring
            </div>
        </div>
    </div>
    """

def create_3d_metric_card(title: str, value: str, change: str, icon: str = "📊"):
    """Create a 3D animated metric card"""
    return f"""
    <div class="metric-card-3d">
        <div class="metric-card-inner">
            <div class="metric-icon">{icon}</div>
            <div class="metric-content">
                <h3 class="metric-title">{title}</h3>
                <div class="metric-value">{value}</div>
                <div class="metric-change">{change}</div>
            </div>
            <div class="metric-glow"></div>
        </div>
    </div>
    """

def create_3d_feature_card(title: str, description: str, icon: str, color: str = "primary"):
    """Create a 3D feature card with hover effects"""
    return f"""
    <div class="feature-card-3d feature-{color}">
        <div class="feature-card-inner">
            <div class="feature-icon">{icon}</div>
            <h3 class="feature-title">{title}</h3>
            <p class="feature-description">{description}</p>
            <div class="feature-glow"></div>
        </div>
    </div>
    """

def create_3d_parallax_section():
    """Create a 3D parallax section with layered elements"""
    return """
    <div class="parallax-section">
        <div class="parallax-layer layer-1"></div>
        <div class="parallax-layer layer-2"></div>
        <div class="parallax-layer layer-3"></div>
        <div class="parallax-content">
            <h2>Advanced Technology Stack</h2>
            <p>Powered by cutting-edge AI and machine learning</p>
        </div>
    </div>
    """

def create_3d_data_visualization(data: Dict, chart_type: str = "health_score"):
    """Create 3D data visualizations"""
    if chart_type == "health_score":
        return create_3d_health_gauge(data)
    elif chart_type == "risk_distribution":
        return create_3d_risk_chart(data)
    elif chart_type == "trend_analysis":
        return create_3d_trend_chart(data)
    else:
        return create_3d_default_chart(data)

def create_3d_health_gauge(data: Dict):
    """Create a 3D health score gauge"""
    fig = go.Figure()
    
    # Create 3D gauge
    theta = np.linspace(0, np.pi, 100)
    r = np.ones_like(theta)
    
    # Health score value (0-100)
    health_score = data.get('health_score', 75)
    angle = (health_score / 100) * np.pi
    
    # Create gauge surface
    fig.add_trace(go.Surface(
        x=r * np.cos(theta),
        y=r * np.sin(theta),
        z=np.zeros_like(theta),
        colorscale='RdYlGn',
        showscale=False,
        opacity=0.8
    ))
    
    # Add needle
    needle_x = [0, 0.8 * np.cos(angle)]
    needle_y = [0, 0.8 * np.sin(angle)]
    needle_z = [0, 0.1]
    
    fig.add_trace(go.Scatter3d(
        x=needle_x,
        y=needle_y,
        z=needle_z,
        mode='lines',
        line=dict(color='red', width=5),
        showlegend=False
    ))
    
    fig.update_layout(
        title=f"Health Score: {health_score}/100",
        scene=dict(
            xaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            yaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            zaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    
    return fig

def create_3d_risk_chart(data: Dict):
    """Create a 3D risk distribution chart"""
    risk_levels = data.get('risk_distribution', {
        'Low Risk': 30,
        'Medium Risk': 45,
        'High Risk': 25
    })
    
    fig = go.Figure()
    
    # Create 3D pie chart
    labels = list(risk_levels.keys())
    values = list(risk_levels.values())
    colors = ['#00ff88', '#ffaa00', '#ff4444']
    
    fig.add_trace(go.Surface(
        x=[[0, 1], [0, 1]],
        y=[[0, 0], [1, 1]],
        z=[[0, 0], [0, 0]],
        colorscale=[[0, colors[0]], [0.5, colors[1]], [1, colors[2]]],
        showscale=False,
        opacity=0.8
    ))
    
    fig.update_layout(
        title="Risk Distribution",
        scene=dict(
            xaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            yaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            zaxis=dict(showgrid=False, showticklabels=False, showbackground=False),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    
    return fig

def create_3d_trend_chart(data: Dict):
    """Create a 3D trend analysis chart"""
    dates = data.get('dates', [])
    values = data.get('values', [])
    
    fig = go.Figure()
    
    # Create 3D line chart
    fig.add_trace(go.Scatter3d(
        x=dates,
        y=values,
        z=np.zeros_like(values),
        mode='lines+markers',
        line=dict(color='#667eea', width=5),
        marker=dict(size=8, color='#667eea'),
        name='Health Score Trend'
    ))
    
    fig.update_layout(
        title="Health Score Trend",
        scene=dict(
            xaxis=dict(title="Date"),
            yaxis=dict(title="Health Score"),
            zaxis=dict(title=""),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    
    return fig

def create_3d_default_chart(data: Dict):
    """Create a default 3D chart"""
    fig = go.Figure()
    
    # Create a simple 3D scatter plot
    x = np.random.randn(50)
    y = np.random.randn(50)
    z = np.random.randn(50)
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=8,
            color=z,
            colorscale='Viridis',
            opacity=0.8
        ),
        name='Data Points'
    ))
    
    fig.update_layout(
        title="3D Data Visualization",
        scene=dict(
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=400
    )
    
    return fig

def create_floating_elements():
    """Create floating 3D elements for background"""
    return """
    <div class="floating-elements">
        <div class="floating-element element-1"></div>
        <div class="floating-element element-2"></div>
        <div class="floating-element element-3"></div>
        <div class="floating-element element-4"></div>
        <div class="floating-element element-5"></div>
    </div>
    """

def create_3d_navigation():
    """Create 3D navigation menu"""
    return """
    <nav class="nav-3d">
        <div class="nav-item nav-item-1">
            <span class="nav-icon">🏠</span>
            <span class="nav-text">Home</span>
        </div>
        <div class="nav-item nav-item-2">
            <span class="nav-icon">🎮</span>
            <span class="nav-text">Demo</span>
        </div>
        <div class="nav-item nav-item-3">
            <span class="nav-icon">📊</span>
            <span class="nav-text">Analytics</span>
        </div>
        <div class="nav-item nav-item-4">
            <span class="nav-icon">🔬</span>
            <span class="nav-text">Technology</span>
        </div>
    </nav>
    """

def create_3d_loading_animation():
    """Create a 3D loading animation"""
    return """
    <div class="loading-3d">
        <div class="loading-cube">
            <div class="cube-face front"></div>
            <div class="cube-face back"></div>
            <div class="cube-face right"></div>
            <div class="cube-face left"></div>
            <div class="cube-face top"></div>
            <div class="cube-face bottom"></div>
        </div>
    </div>
    """

def create_3d_success_animation():
    """Create a 3D success animation"""
    return """
    <div class="success-3d">
        <div class="success-checkmark">
            <div class="check-icon">
                <span class="icon-line line-tip"></span>
                <span class="icon-line line-long"></span>
                <div class="icon-circle"></div>
                <div class="icon-fix"></div>
            </div>
        </div>
    </div>
    """ 