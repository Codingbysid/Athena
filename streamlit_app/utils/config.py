"""
🎯 Athena Configuration Management
Centralized configuration for the Athena Streamlit application
"""

import os
from typing import Dict, Any, List
from pathlib import Path

class AthenaConfig:
    """Centralized configuration management for Athena"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment and defaults"""
        
        # Base paths
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.MODELS_DIR = self.BASE_DIR / "models"
        self.STREAMLIT_DIR = self.BASE_DIR / "streamlit_app"
        
        # Model configuration
        self.MODEL_FILES = {
            'ensemble': 'athena_ensemble_model.pkl',
            'xgboost': 'athena_xgb_model.pkl', 
            'lightgbm': 'athena_lgb_model.pkl',
            'scaler': 'athena_robust_scaler.pkl',
            'encoders': 'athena_advanced_encoders.pkl',
            'features': 'athena_advanced_features.json',
            'metadata': 'athena_advanced_metadata.json'
        }
        
        # Application settings
        self.APP_CONFIG = {
            'title': 'Athena - AI Sales Intelligence',
            'icon': '🚀',
            'layout': 'wide',
            'page_title': 'Athena - AI Sales Intelligence',
            'initial_sidebar_state': 'expanded'
        }
        
        # Demo settings
        self.DEMO_CONFIG = {
            'enable_mock_predictions': True,
            'show_warnings': True,
            'auto_refresh': False,
            'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        }
        
        # Validation rules
        self.VALIDATION_RULES = {
            'amount': {
                'min': 1,
                'max': 100000000,  # $100M
                'required': True
            },
            'stages': [
                'Prospecting', 'Qualification', 'Needs Analysis', 'Value Proposition',
                'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'
            ],
            'industries': [
                'Technology', 'Healthcare', 'Financial Services', 'Manufacturing',
                'Retail', 'Education', 'Government', 'Other'
            ],
            'regions': [
                'North America', 'Europe', 'Asia Pacific', 'Latin America', 'Other'
            ],
            'numeric_fields': {
                'DaysInStage': {'min': 0, 'max': 730, 'default': 0},
                'EmailOpens': {'min': 0, 'max': 200, 'default': 0},
                'EmailClicks': {'min': 0, 'max': 100, 'default': 0},
                'ContentDownloads': {'min': 0, 'max': 50, 'default': 0},
                'MeetingsScheduled': {'min': 0, 'max': 50, 'default': 0},
                'CallsMade': {'min': 0, 'max': 100, 'default': 0},
                'SupportCases': {'min': 0, 'max': 20, 'default': 0},
                'CriticalCases': {'min': 0, 'max': 10, 'default': 0},
                'AvgCaseAge': {'min': 0, 'max': 90, 'default': 0},
                'CloseDatePushed': {'min': 0, 'max': 10, 'default': 0},
                'LastActivityDays': {'min': 0, 'max': 90, 'default': 0},
                'CommunicationFrequency': {'min': 0, 'max': 20, 'default': 0}
            }
        }
        
        # Risk thresholds
        self.RISK_THRESHOLDS = {
            'low_risk': 80,
            'medium_risk': 60,
            'high_risk': 40,
            'critical_risk': 0
        }
        
        # Industry win rates (used for feature engineering)
        self.INDUSTRY_WIN_RATES = {
            'Technology': 0.45,
            'Healthcare': 0.42,
            'Financial Services': 0.38,
            'Manufacturing': 0.40,
            'Retail': 0.35,
            'Education': 0.50,
            'Government': 0.30,
            'Other': 0.35
        }
        
        # Stage order mapping
        self.STAGE_ORDER_MAP = {
            'Prospecting': 1,
            'Qualification': 2,
            'Needs Analysis': 3,
            'Value Proposition': 4,
            'Proposal': 5,
            'Negotiation': 6,
            'Closed Won': 7,
            'Closed Lost': 0
        }
        
        # Deal size categories
        self.DEAL_SIZE_CATEGORIES = {
            'bins': [0, 50000, 200000, 500000, float('inf')],
            'labels': ['Small', 'Medium', 'Large', 'Enterprise']
        }
        
        # Feature engineering weights
        self.FEATURE_WEIGHTS = {
            'email_opens': 0.3,
            'email_clicks': 0.7,
            'content_downloads': 1.5,
            'stalled_threshold': 60,
            'overdue_threshold': 14,
            'risk_weights': {
                'stalled': 0.3,
                'overdue': 0.2,
                'critical_issues': 0.4,
                'communication_gap': 0.1
            }
        }
        
        # UI/UX settings
        self.UI_CONFIG = {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'success_color': '#4facfe',
            'warning_color': '#fa709a',
            'danger_color': '#ff6b6b',
            'border_radius': '15px',
            'animation_duration': '0.3s'
        }
        
        # Cache settings
        self.CACHE_CONFIG = {
            'model_service_ttl': 3600,  # 1 hour
            'sample_data_ttl': 3600,     # 1 hour
            'portfolio_analysis_ttl': 300,  # 5 minutes
            'analytics_data_ttl': 1800,     # 30 minutes
            'chart_data_ttl': 600           # 10 minutes
        }
        
        # Error messages
        self.ERROR_MESSAGES = {
            'model_load_failed': "Failed to load ML models. Using demo mode.",
            'prediction_failed': "Prediction failed. Please try again.",
            'validation_failed': "Invalid input data. Please check your values.",
            'service_unavailable': "Service temporarily unavailable.",
            'demo_mode_active': "Running in demo mode with mock predictions."
        }
        
        # Success messages
        self.SUCCESS_MESSAGES = {
            'prediction_complete': "Analysis complete!",
            'models_loaded': "Models loaded successfully",
            'demo_ready': "Demo mode ready"
        }
    
    def get_model_path(self, model_name: str) -> Path:
        """Get the full path to a model file"""
        if model_name not in self.MODEL_FILES:
            raise ValueError(f"Unknown model: {model_name}")
        return self.MODELS_DIR / self.MODEL_FILES[model_name]
    
    def get_validation_rule(self, field: str) -> Dict[str, Any]:
        """Get validation rules for a specific field"""
        if field in self.VALIDATION_RULES['numeric_fields']:
            return self.VALIDATION_RULES['numeric_fields'][field]
        return {}
    
    def get_risk_level(self, health_score: int) -> str:
        """Determine risk level based on health score"""
        if health_score >= self.RISK_THRESHOLDS['low_risk']:
            return "Low Risk"
        elif health_score >= self.RISK_THRESHOLDS['medium_risk']:
            return "Medium Risk"
        elif health_score >= self.RISK_THRESHOLDS['high_risk']:
            return "High Risk"
        else:
            return "Critical Risk"
    
    def get_industry_win_rate(self, industry: str) -> float:
        """Get win rate for a specific industry"""
        return self.INDUSTRY_WIN_RATES.get(industry, 0.35)
    
    def get_stage_order(self, stage: str) -> int:
        """Get order number for a sales stage"""
        return self.STAGE_ORDER_MAP.get(stage, 3)
    
    def is_valid_stage(self, stage: str) -> bool:
        """Check if stage is valid"""
        return stage in self.VALIDATION_RULES['stages']
    
    def is_valid_industry(self, industry: str) -> bool:
        """Check if industry is valid"""
        return industry in self.VALIDATION_RULES['industries']
    
    def is_valid_region(self, region: str) -> bool:
        """Check if region is valid"""
        return region in self.VALIDATION_RULES['regions']
    
    def get_error_message(self, error_type: str) -> str:
        """Get user-friendly error message"""
        return self.ERROR_MESSAGES.get(error_type, "An error occurred")
    
    def get_success_message(self, success_type: str) -> str:
        """Get user-friendly success message"""
        return self.SUCCESS_MESSAGES.get(success_type, "Operation completed successfully")

# Global configuration instance
_config = None

def get_config() -> AthenaConfig:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = AthenaConfig()
    return _config 