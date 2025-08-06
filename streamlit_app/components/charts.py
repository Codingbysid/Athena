"""
Interactive Charts and Visualizations for Athena Streamlit App
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any

def create_health_score_gauge(health_score: int, risk_level: str) -> go.Figure:
    """Create an enhanced gauge chart for health score with trend indicators"""
    
    # Color based on risk level
    color_map = {
        "Low Risk": "green",
        "Medium Risk": "orange", 
        "High Risk": "red",
        "Critical Risk": "darkred"
    }
    
    color = color_map.get(risk_level, "gray")
    
    # Determine trend indicator
    if health_score >= 80:
        trend_emoji = "🚀"
        trend_text = "Excellent"
    elif health_score >= 60:
        trend_emoji = "📈"
        trend_text = "Good"
    elif health_score >= 40:
        trend_emoji = "⚠️"
        trend_text = "Needs Attention"
    else:
        trend_emoji = "🚨"
        trend_text = "Critical"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = health_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': f"Health Score<br><span style='font-size:0.8em;color:{color}'>{risk_level}</span><br><span style='font-size:0.7em;color:gray'>{trend_emoji} {trend_text}</span>"
        },
        delta = {'reference': 50, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 60], 'color': "lightyellow"},
                {'range': [60, 80], 'color': "lightgreen"},
                {'range': [80, 100], 'color': "darkgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    # Add annotations for better context
    annotations = [
        dict(
            x=0.5, y=0.1, xref='paper', yref='paper',
            text=f"Target: 80+ | Warning: 60+ | Critical: <40",
            showarrow=False,
            font=dict(size=10, color="gray"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        )
    ]
    
    fig.update_layout(
        height=400,
        font={'color': "darkblue", 'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=annotations
    )
    
    return fig

def create_risk_distribution_pie(opportunities: List[Dict]) -> go.Figure:
    """Create pie chart showing risk distribution"""
    
    # Count risk levels
    risk_counts = {}
    for opp in opportunities:
        risk_level = opp.get('risk_level', 'Unknown')
        risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
    
    if not risk_counts:
        # Default data for demo
        risk_counts = {
            'Low Risk': 45,
            'Medium Risk': 30,
            'High Risk': 20,
            'Critical Risk': 5
        }
    
    colors = ['#2E8B57', '#FF8C00', '#DC143C', '#8B0000']
    
    fig = go.Figure(data=[go.Pie(
        labels=list(risk_counts.keys()),
        values=list(risk_counts.values()),
        hole=.3,
        marker_colors=colors
    )])
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title="Risk Distribution Across Portfolio",
        annotations=[dict(text='Risk<br>Levels', x=0.5, y=0.5, font_size=16, showarrow=False)],
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_health_trend_chart(days: int = 30) -> go.Figure:
    """Create a trend chart for health scores over time with enhanced indicators"""
    
    # Generate sample trend data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
    
    # Simulate realistic health score trends
    np.random.seed(42)
    base_score = 65
    trend = np.cumsum(np.random.normal(0, 2, days))
    noise = np.random.normal(0, 5, days)
    scores = base_score + trend + noise
    scores = np.clip(scores, 0, 100)
    
    fig = go.Figure()
    
    # Add main health score line
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Portfolio Health Score',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6),
        hovertemplate='<b>Date:</b> %{x}<br><b>Health Score:</b> %{y:.1f}<extra></extra>'
    ))
    
    # Add trend line
    z = np.polyfit(range(len(scores)), scores, 1)
    trend_line = np.poly1d(z)(range(len(scores)))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=trend_line,
        mode='lines',
        name='Trend Line',
        line=dict(color='red', width=2, dash='dash'),
        hovertemplate='<b>Trend:</b> %{y:.1f}<extra></extra>'
    ))
    
    # Add moving average for smoother trend
    window = min(7, len(scores) // 4)
    if window > 1:
        moving_avg = pd.Series(scores).rolling(window=window).mean()
        fig.add_trace(go.Scatter(
            x=dates,
            y=moving_avg,
            mode='lines',
            name=f'{window}-Day Moving Avg',
            line=dict(color='green', width=2),
            hovertemplate='<b>Moving Avg:</b> %{y:.1f}<extra></extra>'
        ))
    
    # Add threshold lines
    fig.add_hline(y=80, line_dash="dot", line_color="green", 
                  annotation_text="Target (80)", annotation_position="top right")
    fig.add_hline(y=60, line_dash="dot", line_color="orange", 
                  annotation_text="Warning (60)", annotation_position="top right")
    fig.add_hline(y=40, line_dash="dot", line_color="red", 
                  annotation_text="Critical (40)", annotation_position="top right")
    
    # Add trend indicator
    trend_direction = "↗️ Improving" if trend_line[-1] > trend_line[0] else "↘️ Declining"
    trend_strength = abs(trend_line[-1] - trend_line[0]) / len(trend_line)
    trend_text = f"{trend_direction} ({trend_strength:.1f} points/day)"
    
    fig.update_layout(
        title=f"Portfolio Health Score Trend - {trend_text}",
        xaxis_title="Date",
        yaxis_title="Health Score",
        yaxis=dict(range=[0, 100]),
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hovermode='x unified',
        annotations=[
            dict(
                x=0.02, y=0.98, xref='paper', yref='paper',
                text=f"Current: {scores[-1]:.1f}",
                showarrow=False,
                font=dict(size=12, color="blue"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="blue",
                borderwidth=1
            )
        ]
    )
    
    return fig

def create_feature_importance_chart(model_service) -> go.Figure:
    """Create feature importance chart"""
    
    # Sample feature importance (replace with actual model feature importance)
    features = [
        'StageName', 'StageOrder', 'HasCriticalIssues', 'CriticalCases',
        'StageProgress', 'DealVelocity', 'IndustryWinRate', 'RiskScore',
        'IsOverdue', 'CommunicationGap', 'EngagementScore', 'TotalCalls'
    ]
    
    importance = [0.115, 0.100, 0.083, 0.055, 0.054, 0.040, 0.039, 0.033, 0.022, 0.021, 0.018, 0.015]
    
    # Sort by importance
    sorted_data = sorted(zip(features, importance), key=lambda x: x[1], reverse=True)
    features_sorted = [x[0] for x in sorted_data]
    importance_sorted = [x[1] for x in sorted_data]
    
    fig = go.Figure(go.Bar(
        x=importance_sorted,
        y=features_sorted,
        orientation='h',
        marker_color=px.colors.sequential.Viridis
    ))
    
    fig.update_layout(
        title="Top Features Driving Health Scores",
        xaxis_title="Feature Importance",
        yaxis_title="Features",
        height=500,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_industry_performance_chart() -> go.Figure:
    """Create industry performance comparison chart"""
    
    industries = ['Technology', 'Healthcare', 'Financial Services', 'Manufacturing', 
                 'Retail', 'Education', 'Government', 'Other']
    avg_health = [72, 68, 61, 65, 58, 75, 52, 60]
    win_rates = [45, 42, 38, 40, 35, 50, 30, 35]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Avg Health Score',
        x=industries,
        y=avg_health,
        yaxis='y',
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Scatter(
        name='Win Rate (%)',
        x=industries,
        y=win_rates,
        yaxis='y2',
        mode='lines+markers',
        marker_color='red',
        line=dict(width=3)
    ))
    
    fig.update_layout(
        title="Performance by Industry",
        xaxis_title="Industry",
        yaxis=dict(
            title="Average Health Score",
            side="left",
            range=[0, 100]
        ),
        yaxis2=dict(
            title="Win Rate (%)",
            side="right",
            overlaying="y",
            range=[0, 60]
        ),
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(x=0.01, y=0.99)
    )
    
    fig.update_xaxis(tickangle=45)
    
    return fig

def create_deal_value_vs_health_scatter() -> go.Figure:
    """Create scatter plot of deal value vs health score"""
    
    # Generate sample data
    np.random.seed(42)
    n_deals = 100
    
    health_scores = np.random.normal(65, 20, n_deals)
    health_scores = np.clip(health_scores, 0, 100)
    
    # Correlation between health and deal size
    base_amounts = np.random.exponential(200000, n_deals)
    health_effect = health_scores / 100
    deal_amounts = base_amounts * (0.5 + health_effect)
    
    # Risk levels
    risk_levels = []
    colors = []
    for score in health_scores:
        if score >= 80:
            risk_levels.append("Low Risk")
            colors.append("green")
        elif score >= 60:
            risk_levels.append("Medium Risk")
            colors.append("orange")
        elif score >= 40:
            risk_levels.append("High Risk")
            colors.append("red")
        else:
            risk_levels.append("Critical Risk")
            colors.append("darkred")
    
    fig = go.Figure()
    
    for risk_level in ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]:
        mask = [r == risk_level for r in risk_levels]
        if any(mask):
            x_vals = [health_scores[i] for i, m in enumerate(mask) if m]
            y_vals = [deal_amounts[i] for i, m in enumerate(mask) if m]
            color = colors[risk_levels.index(risk_level)]
            
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='markers',
                name=risk_level,
                marker=dict(
                    size=8,
                    color=color,
                    opacity=0.7
                ),
                hovertemplate=f'<b>{risk_level}</b><br>Health Score: %{{x:.1f}}<br>Deal Value: $%{{y:,.0f}}<extra></extra>'
            ))
    
    fig.update_layout(
        title="Deal Value vs Health Score",
        xaxis_title="Health Score",
        yaxis_title="Deal Value ($)",
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_rescue_impact_chart() -> go.Figure:
    """Create chart showing impact of rescue interventions"""
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    deals_at_risk = [45, 52, 48, 61, 55, 58]
    deals_rescued = [12, 18, 15, 22, 19, 24]
    rescue_rate = [r/total*100 for r, total in zip(deals_rescued, deals_at_risk)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Deals at Risk',
        x=months,
        y=deals_at_risk,
        marker_color='lightcoral'
    ))
    
    fig.add_trace(go.Bar(
        name='Deals Rescued',
        x=months,
        y=deals_rescued,
        marker_color='lightgreen'
    ))
    
    fig.add_trace(go.Scatter(
        name='Rescue Rate (%)',
        x=months,
        y=rescue_rate,
        yaxis='y2',
        mode='lines+markers',
        marker_color='blue',
        line=dict(width=3)
    ))
    
    fig.update_layout(
        title="Rescue Intervention Impact",
        xaxis_title="Month",
        yaxis=dict(
            title="Number of Deals",
            side="left"
        ),
        yaxis2=dict(
            title="Rescue Rate (%)",
            side="right",
            overlaying="y"
        ),
        height=400,
        font={'family': "Arial"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        barmode='group'
    )
    
    return fig