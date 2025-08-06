"""
Athena ML Models Integration for Streamlit
Integrates the existing Athena ensemble models with Streamlit app
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
import json
from typing import Dict, Any, Tuple, Optional
import logging
import traceback
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

# Add the scripts directory to the path to import existing modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# Import configuration
from config import get_config

# Custom exceptions for better error handling
class AthenaModelError(Exception):
    """Base exception for Athena model errors"""
    pass

class ModelLoadError(AthenaModelError):
    """Raised when model loading fails"""
    pass

class PredictionError(AthenaModelError):
    """Raised when prediction fails"""
    pass

class DataValidationError(AthenaModelError):
    """Raised when input data validation fails"""
    pass

class AthenaModelService:
    """Service class to handle Athena ML model predictions"""
    
    def __init__(self, models_dir: str = None):
        # Get configuration
        self.config = get_config()
        
        if models_dir is None:
            self.models_dir = self.config.MODELS_DIR
        else:
            self.models_dir = models_dir
            
        self.xgb_model = None
        self.lgb_model = None
        self.ensemble_model = None
        self.scaler = None
        self.encoders = None
        self.feature_names = None
        self.metadata = None
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_models(self) -> bool:
        """Load all Athena models and artifacts with comprehensive error handling"""
        if not os.path.exists(self.models_dir):
            raise ModelLoadError(f"Models directory not found: {self.models_dir}")
        
        models_loaded = 0
        total_models = 0
        
        try:
            # Load models using configuration
            for model_name, model_file in self.config.MODEL_FILES.items():
                if model_name in ['ensemble', 'xgboost', 'lightgbm']:
                    total_models += 1
                
                model_path = self.models_dir / model_file
                
                if os.path.exists(model_path):
                    try:
                        if model_name == 'ensemble':
                            self.ensemble_model = joblib.load(model_path)
                            models_loaded += 1
                            self.logger.info("✅ Ensemble model loaded successfully")
                        elif model_name == 'xgboost':
                            self.xgb_model = joblib.load(model_path)
                            models_loaded += 1
                            self.logger.info("✅ XGBoost model loaded successfully")
                        elif model_name == 'lightgbm':
                            self.lgb_model = joblib.load(model_path)
                            models_loaded += 1
                            self.logger.info("✅ LightGBM model loaded successfully")
                        elif model_name == 'scaler':
                            self.scaler = joblib.load(model_path)
                            self.logger.info("✅ Scaler loaded successfully")
                        elif model_name == 'encoders':
                            self.encoders = joblib.load(model_path)
                            self.logger.info("✅ Encoders loaded successfully")
                        elif model_name == 'features':
                            with open(model_path, 'r') as f:
                                self.feature_names = json.load(f)
                            self.logger.info("✅ Feature names loaded successfully")
                        elif model_name == 'metadata':
                            with open(model_path, 'r') as f:
                                self.metadata = json.load(f)
                            self.logger.info("✅ Model metadata loaded successfully")
                    except Exception as e:
                        if model_name in ['ensemble', 'xgboost', 'lightgbm']:
                            self.logger.warning(f"⚠️ Failed to load {model_name} model: {str(e)}")
                        else:
                            self.logger.warning(f"⚠️ Failed to load {model_name}: {str(e)}")
                else:
                    if model_name in ['ensemble', 'xgboost', 'lightgbm']:
                        self.logger.warning(f"⚠️ {model_name} model file not found: {model_path}")
                    else:
                        self.logger.warning(f"⚠️ {model_name} file not found: {model_path}")
            
            # Validate that at least one model was loaded
            if models_loaded == 0:
                raise ModelLoadError("No ML models could be loaded successfully")
            
            self.logger.info(f"✅ Successfully loaded {models_loaded}/{total_models} ML models")
            return True
            
        except ModelLoadError:
            raise
        except Exception as e:
            self.logger.error(f"❌ Unexpected error loading models: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise ModelLoadError(f"Failed to load models: {str(e)}")
    
    def validate_input_data(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean input data using configuration"""
        if not isinstance(opportunity_data, dict):
            raise DataValidationError("Input data must be a dictionary")
        
        # Check required fields
        required_fields = ['Amount', 'StageName', 'Industry']
        for field in required_fields:
            if field not in opportunity_data:
                raise DataValidationError(f"Missing required field: {field}")
        
        # Validate data types and ranges
        cleaned_data = opportunity_data.copy()
        
        # Amount validation using config
        try:
            cleaned_data['Amount'] = float(cleaned_data['Amount'])
            amount_rules = self.config.VALIDATION_RULES['amount']
            if cleaned_data['Amount'] <= amount_rules['min']:
                raise DataValidationError(f"Amount must be greater than ${amount_rules['min']:,}")
            if cleaned_data['Amount'] > amount_rules['max']:
                self.logger.warning(f"Unusually large deal amount: ${cleaned_data['Amount']:,.0f}")
        except (ValueError, TypeError):
            raise DataValidationError("Amount must be a valid number")
        
        # Stage validation using config
        if not self.config.is_valid_stage(cleaned_data['StageName']):
            self.logger.warning(f"Unknown stage: {cleaned_data['StageName']}, using default")
            cleaned_data['StageName'] = 'Qualification'
        
        # Industry validation using config
        if not self.config.is_valid_industry(cleaned_data['Industry']):
            self.logger.warning(f"Unknown industry: {cleaned_data['Industry']}, using 'Other'")
            cleaned_data['Industry'] = 'Other'
        
        # Fill missing optional fields with safe defaults using config
        for field, rules in self.config.VALIDATION_RULES['numeric_fields'].items():
            if field not in cleaned_data or cleaned_data[field] is None:
                cleaned_data[field] = rules['default']
            else:
                try:
                    value = float(cleaned_data[field])
                    # Ensure value is within bounds
                    value = max(rules['min'], min(rules['max'], value))
                    cleaned_data[field] = value
                except (ValueError, TypeError):
                    self.logger.warning(f"Invalid value for {field}, using default: {rules['default']}")
                    cleaned_data[field] = rules['default']
        
        # Validate ranges for specific fields
        days_rules = self.config.get_validation_rule('DaysInStage')
        if cleaned_data['DaysInStage'] > days_rules.get('max', 730):
            self.logger.warning(f"Unusually long time in stage: {cleaned_data['DaysInStage']} days")
        
        activity_rules = self.config.get_validation_rule('LastActivityDays')
        if cleaned_data['LastActivityDays'] > activity_rules.get('max', 365):
            self.logger.warning(f"Very long time since last activity: {cleaned_data['LastActivityDays']} days")
        
        return cleaned_data

    def engineer_features(self, opportunity_data: Dict[str, Any]) -> pd.DataFrame:
        """Engineer features from opportunity data with error handling"""
        try:
            # Validate input data first
            cleaned_data = self.validate_input_data(opportunity_data)
            
            # Convert to DataFrame
            df = pd.DataFrame([cleaned_data])
            
            # Basic feature engineering using configuration
            df['DealVelocity'] = df['Amount'] / (df['DaysInStage'] + 1)
            
            # Engagement score using config weights
            weights = self.config.FEATURE_WEIGHTS
            df['EngagementScore'] = (
                df['EmailOpens'] * weights['email_opens'] + 
                df['EmailClicks'] * weights['email_clicks'] + 
                df['ContentDownloads'] * weights['content_downloads']
            )
            
            df['CommunicationGap'] = df['LastActivityDays']
            df['TotalCalls'] = df['CallsMade'] 
            df['TotalMeetings'] = df['MeetingsScheduled']
            df['TotalEmailEngagement'] = df['EmailOpens'] + df['EmailClicks']
            
            # Risk indicators using config thresholds
            df['IsStalled'] = (df['DaysInStage'] > weights['stalled_threshold']).astype(int)
            df['IsOverdue'] = (df['LastActivityDays'] > weights['overdue_threshold']).astype(int)
            df['HasCriticalIssues'] = (df['CriticalCases'] > 0).astype(int)
            
            # Stage mapping using config
            df['StageOrder'] = df['StageName'].map(self.config.STAGE_ORDER_MAP).fillna(3)
            
            # Industry win rates using config
            df['IndustryWinRate'] = df['Industry'].map(self.config.INDUSTRY_WIN_RATES).fillna(0.35)
            
            # Deal size categories using config
            try:
                df['DealSizeCategory'] = pd.cut(
                    df['Amount'], 
                    bins=self.config.DEAL_SIZE_CATEGORIES['bins'],
                    labels=self.config.DEAL_SIZE_CATEGORIES['labels']
                ).astype(str)  # Convert to string to avoid categorical issues
            except Exception:
                # Fallback for edge cases
                df['DealSizeCategory'] = 'Medium'
            
            # Risk score calculation using config weights
            risk_weights = weights['risk_weights']
            df['RiskScore'] = (
                df['IsStalled'] * risk_weights['stalled'] +
                df['IsOverdue'] * risk_weights['overdue'] +
                df['HasCriticalIssues'] * risk_weights['critical_issues'] +
                (df['CommunicationGap'] / 30) * risk_weights['communication_gap']
            )
            
            # Additional advanced features
            df['StageProgress'] = df['StageOrder'] / 7.0
            df['CriticalCases'] = df['CriticalCases']
            df['AvgCaseAge'] = df['AvgCaseAge']
            df['CloseDatePushed'] = df['CloseDatePushed']
            
            # Ensure no infinite or NaN values
            df = df.replace([np.inf, -np.inf], 0)
            df = df.fillna(0)
            
            return df
            
        except DataValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Error engineering features: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise PredictionError(f"Feature engineering failed: {str(e)}")
    
    def predict_health_score(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict opportunity health score with comprehensive error handling"""
        try:
            # Check if any models are loaded
            if not any([self.ensemble_model, self.xgb_model, self.lgb_model]):
                raise PredictionError("No ML models are loaded. Please load models first.")
            
            # Engineer features (includes validation)
            df = self.engineer_features(opportunity_data)
            
            # Handle categorical encoding
            if self.encoders:
                for column, encoder in self.encoders.items():
                    if column in df.columns:
                        try:
                            df[column] = encoder.transform(df[column])
                        except ValueError as e:
                            # Handle unseen categories gracefully
                            self.logger.warning(f"Unseen category in {column}: {df[column].iloc[0]}, using default value 0")
                            df[column] = 0
                        except Exception as e:
                            self.logger.warning(f"Error encoding {column}: {str(e)}, using default value 0")
                            df[column] = 0
            
            # Select features that the model expects
            if self.feature_names:
                # Ensure all required features exist
                missing_features = []
                for feature in self.feature_names:
                    if feature not in df.columns:
                        df[feature] = 0
                        missing_features.append(feature)
                
                if missing_features:
                    self.logger.warning(f"Missing features set to 0: {missing_features}")
                
                # Select only the features the model was trained on
                X = df[self.feature_names]
            else:
                # Fallback: use numerical columns
                X = df.select_dtypes(include=[np.number])
                if X.empty:
                    raise PredictionError("No numerical features found for prediction")
            
            # Validate feature matrix
            if X.isnull().any().any():
                self.logger.warning("Found null values in features, filling with 0")
                X = X.fillna(0)
            
            if np.isinf(X.values).any():
                self.logger.warning("Found infinite values in features, replacing with 0")
                X = X.replace([np.inf, -np.inf], 0)
            
            # Scale features
            try:
                if self.scaler:
                    X_scaled = self.scaler.transform(X)
                else:
                    X_scaled = X.values
            except Exception as e:
                self.logger.warning(f"Error scaling features: {str(e)}, using unscaled features")
                X_scaled = X.values
            
            # Make predictions with fallback handling
            predictions = {}
            prediction_errors = []
            
            # Try ensemble model first (highest priority)
            if self.ensemble_model:
                try:
                    ensemble_prob = self.ensemble_model.predict_proba(X_scaled)[0][1]
                    predictions['ensemble'] = float(ensemble_prob)
                except Exception as e:
                    prediction_errors.append(f"Ensemble model failed: {str(e)}")
                    self.logger.warning(f"Ensemble prediction failed: {str(e)}")
            
            # Try XGBoost model
            if self.xgb_model:
                try:
                    xgb_prob = self.xgb_model.predict_proba(X_scaled)[0][1]
                    predictions['xgb'] = float(xgb_prob)
                except Exception as e:
                    prediction_errors.append(f"XGBoost model failed: {str(e)}")
                    self.logger.warning(f"XGBoost prediction failed: {str(e)}")
            
            # Try LightGBM model
            if self.lgb_model:
                try:
                    lgb_prob = self.lgb_model.predict_proba(X_scaled)[0][1]
                    predictions['lightgbm'] = float(lgb_prob)
                except Exception as e:
                    prediction_errors.append(f"LightGBM model failed: {str(e)}")
                    self.logger.warning(f"LightGBM prediction failed: {str(e)}")
            
            # Check if we got any predictions
            if not predictions:
                error_summary = "; ".join(prediction_errors)
                raise PredictionError(f"All models failed to make predictions. Errors: {error_summary}")
            
            # Calculate final probability
            if 'ensemble' in predictions:
                final_probability = predictions['ensemble']
            elif len(predictions) > 1:
                final_probability = np.mean(list(predictions.values()))
            else:
                final_probability = list(predictions.values())[0]
            
            # Validate probability is in valid range
            final_probability = max(0.0, min(1.0, final_probability))
            
            # Convert to health score (0-100)
            health_score = int(round(final_probability * 100))
            health_score = max(0, min(100, health_score))  # Ensure within bounds
            
            # Determine risk level using configuration
            risk_level = self.config.get_risk_level(health_score)
            
            return {
                'health_score': health_score,
                'probability': final_probability,
                'risk_level': risk_level,
                'model_predictions': predictions,
                'opportunity_id': opportunity_data.get('Id', 'Unknown'),
                'models_used': list(predictions.keys()),
                'prediction_warnings': prediction_errors if prediction_errors else None
            }
            
        except (DataValidationError, PredictionError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error making prediction: {str(e)}")
            self.logger.debug(traceback.format_exc())
            raise PredictionError(f"Prediction failed: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        info = {
            'models_loaded': {
                'ensemble': self.ensemble_model is not None,
                'xgboost': self.xgb_model is not None,
                'lightgbm': self.lgb_model is not None
            },
            'artifacts_loaded': {
                'scaler': self.scaler is not None,
                'encoders': self.encoders is not None,
                'features': self.feature_names is not None,
                'metadata': self.metadata is not None
            }
        }
        
        if self.metadata:
            info['performance'] = self.metadata
            
        return info

# Global model service instance
_model_service = None
_model_service_error = None

def get_model_service() -> AthenaModelService:
    """Get the global model service instance with error handling"""
    global _model_service, _model_service_error
    
    if _model_service is None:
        try:
            _model_service = AthenaModelService()
            if not _model_service.load_models():
                raise ModelLoadError("Failed to load any models")
            _model_service_error = None  # Clear any previous errors
        except Exception as e:
            _model_service_error = str(e)
            # Return a mock service for demo purposes if models fail to load
            _model_service = MockModelService()
            logging.warning(f"Using mock model service due to error: {str(e)}")
    
    return _model_service

def get_model_service_status() -> Dict[str, Any]:
    """Get the status of the model service"""
    global _model_service, _model_service_error
    
    if _model_service_error:
        return {
            'status': 'error',
            'error': _model_service_error,
            'is_mock': isinstance(_model_service, MockModelService)
        }
    elif _model_service is None:
        return {
            'status': 'not_initialized',
            'error': None,
            'is_mock': False
        }
    else:
        return {
            'status': 'ready',
            'error': None,
            'is_mock': isinstance(_model_service, MockModelService)
        }

class MockModelService:
    """Mock model service for demo purposes when real models fail to load"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = logging.getLogger(__name__)
        self.logger.warning("🔧 Using mock model service for demo")
    
    def predict_health_score(self, opportunity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock predictions for demo purposes"""
        try:
            # Basic validation
            if not isinstance(opportunity_data, dict):
                raise DataValidationError("Input data must be a dictionary")
            
            # Generate realistic mock predictions based on input
            amount = float(opportunity_data.get('Amount', 100000))
            stage = opportunity_data.get('StageName', 'Qualification')
            industry = opportunity_data.get('Industry', 'Technology')
            days_in_stage = int(opportunity_data.get('DaysInStage', 30))
            
            # Simple heuristic for mock score
            base_score = 60
            
            # Adjust based on stage
            stage_adjustments = {
                'Prospecting': -20, 'Qualification': -10, 'Needs Analysis': 0,
                'Value Proposition': 5, 'Proposal': 10, 'Negotiation': 15,
                'Closed Won': 90, 'Closed Lost': 0
            }
            base_score += stage_adjustments.get(stage, 0)
            
            # Adjust based on industry
            industry_adjustments = {
                'Technology': 10, 'Healthcare': 5, 'Financial Services': 0,
                'Manufacturing': 5, 'Retail': -5, 'Education': 15,
                'Government': -10, 'Other': 0
            }
            base_score += industry_adjustments.get(industry, 0)
            
            # Adjust based on deal size (larger deals are riskier)
            if amount > 1000000:
                base_score -= 10
            elif amount > 500000:
                base_score -= 5
            
            # Adjust based on time in stage
            if days_in_stage > 90:
                base_score -= 15
            elif days_in_stage > 60:
                base_score -= 10
            
            # Add some randomness
            import random
            base_score += random.randint(-5, 5)
            
            # Ensure score is within bounds
            health_score = max(10, min(95, base_score))
            probability = health_score / 100.0
            
            # Determine risk level using configuration
            risk_level = self.config.get_risk_level(health_score)
            
            return {
                'health_score': health_score,
                'probability': probability,
                'risk_level': risk_level,
                'model_predictions': {'mock': probability},
                'opportunity_id': opportunity_data.get('Id', 'Unknown'),
                'models_used': ['mock'],
                'is_mock_prediction': True,
                'prediction_warnings': ['Using mock predictions - real models failed to load']
            }
            
        except Exception as e:
            raise PredictionError(f"Mock prediction failed: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get mock model info"""
        return {
            'models_loaded': {
                'ensemble': False,
                'xgboost': False,
                'lightgbm': False
            },
            'artifacts_loaded': {
                'scaler': False,
                'encoders': False,
                'features': False,
                'metadata': False
            },
            'is_mock': True,
            'status': 'Mock service for demo purposes'
        }

# Sample data for demos
def get_sample_opportunities():
    """Get sample opportunity data for demos"""
    return [
        {
            'Id': 'DEMO001',
            'Amount': 250000,
            'StageName': 'Proposal',
            'Industry': 'Technology',
            'Region': 'North America',
            'DaysInStage': 30,
            'EmailOpens': 35,
            'EmailClicks': 12,
            'ContentDownloads': 5,
            'MeetingsScheduled': 6,
            'CallsMade': 18,
            'SupportCases': 0,
            'CriticalCases': 0,
            'AvgCaseAge': 0,
            'CloseDatePushed': 0,
            'LastActivityDays': 5,
            'CommunicationFrequency': 12
        },
        {
            'Id': 'DEMO002',
            'Amount': 150000,
            'StageName': 'Negotiation',
            'Industry': 'Healthcare',
            'Region': 'Europe',
            'DaysInStage': 45,
            'EmailOpens': 25,
            'EmailClicks': 8,
            'ContentDownloads': 3,
            'MeetingsScheduled': 4,
            'CallsMade': 12,
            'SupportCases': 1,
            'CriticalCases': 0,
            'AvgCaseAge': 5,
            'CloseDatePushed': 1,
            'LastActivityDays': 15,
            'CommunicationFrequency': 8
        },
        {
            'Id': 'DEMO003',
            'Amount': 500000,
            'StageName': 'Needs Analysis',
            'Industry': 'Financial Services',
            'Region': 'Asia Pacific',
            'DaysInStage': 75,
            'EmailOpens': 15,
            'EmailClicks': 4,
            'ContentDownloads': 1,
            'MeetingsScheduled': 2,
            'CallsMade': 6,
            'SupportCases': 3,
            'CriticalCases': 1,
            'AvgCaseAge': 20,
            'CloseDatePushed': 2,
            'LastActivityDays': 25,
            'CommunicationFrequency': 3
        }
    ]