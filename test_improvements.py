#!/usr/bin/env python3
"""
🧪 Test script to verify Athena improvements
Tests error handling, caching, and configuration management
"""

import sys
import os
from pathlib import Path

# Add the streamlit_app directory to the path
sys.path.append(str(Path(__file__).parent / "streamlit_app" / "utils"))

def test_configuration():
    """Test configuration management"""
    print("🔧 Testing Configuration Management...")
    
    try:
        from config import get_config
        config = get_config()
        
        # Test basic configuration
        assert config.MODELS_DIR.exists() or config.MODELS_DIR.parent.exists(), "Models directory should exist"
        assert len(config.VALIDATION_RULES['stages']) > 0, "Should have validation stages"
        assert len(config.VALIDATION_RULES['industries']) > 0, "Should have validation industries"
        
        # Test risk level determination
        assert config.get_risk_level(85) == "Low Risk", "85 should be Low Risk"
        assert config.get_risk_level(65) == "Medium Risk", "65 should be Medium Risk"
        assert config.get_risk_level(45) == "High Risk", "45 should be High Risk"
        assert config.get_risk_level(15) == "Critical Risk", "15 should be Critical Risk"
        
        # Test validation
        assert config.is_valid_stage("Proposal"), "Proposal should be valid stage"
        assert config.is_valid_industry("Technology"), "Technology should be valid industry"
        assert not config.is_valid_stage("Invalid"), "Invalid should not be valid stage"
        
        print("✅ Configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def test_model_service():
    """Test model service with error handling"""
    print("🤖 Testing Model Service...")
    
    try:
        from athena_models import get_model_service, get_model_service_status, AthenaModelError
        
        # Test service initialization
        service = get_model_service()
        status = get_model_service_status()
        
        assert service is not None, "Model service should be initialized"
        assert 'status' in status, "Status should have status field"
        assert 'is_mock' in status, "Status should have is_mock field"
        
        print(f"✅ Model service initialized: {status['status']}")
        
        # Test prediction with sample data
        sample_data = {
            'Id': 'TEST001',
            'Amount': 100000,
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
        
        result = service.predict_health_score(sample_data)
        
        assert 'health_score' in result, "Result should have health_score"
        assert 'risk_level' in result, "Result should have risk_level"
        assert 'probability' in result, "Result should have probability"
        assert 0 <= result['health_score'] <= 100, "Health score should be 0-100"
        
        print(f"✅ Prediction successful: {result['health_score']}/100 ({result['risk_level']})")
        return True
        
    except Exception as e:
        print(f"❌ Model service test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling with invalid data"""
    print("🛡️ Testing Error Handling...")
    
    try:
        from athena_models import get_model_service, DataValidationError, PredictionError
        
        service = get_model_service()
        
        # Test invalid amount
        try:
            invalid_data = {
                'Id': 'TEST002',
                'Amount': -1000,  # Invalid negative amount
                'StageName': 'Proposal',
                'Industry': 'Technology'
            }
            service.predict_health_score(invalid_data)
            print("❌ Should have raised validation error for negative amount")
            return False
        except DataValidationError:
            print("✅ Correctly caught negative amount error")
        
        # Test missing required field
        try:
            invalid_data = {
                'Id': 'TEST003',
                'Amount': 100000,
                # Missing StageName and Industry
            }
            service.predict_health_score(invalid_data)
            print("❌ Should have raised validation error for missing fields")
            return False
        except DataValidationError:
            print("✅ Correctly caught missing fields error")
        
        # Test invalid stage
        try:
            invalid_data = {
                'Id': 'TEST004',
                'Amount': 100000,
                'StageName': 'InvalidStage',
                'Industry': 'Technology'
            }
            result = service.predict_health_score(invalid_data)
            # Should use default stage instead of failing
            assert result['health_score'] >= 0, "Should still get valid prediction"
            print("✅ Correctly handled invalid stage with default")
        except Exception as e:
            print(f"❌ Should have handled invalid stage gracefully: {str(e)}")
            return False
        
        print("✅ Error handling tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        return False

def test_caching():
    """Test caching functionality"""
    print("⚡ Testing Caching...")
    
    try:
        import streamlit as st
        
        # Test that we can import cached functions
        from athena_models import get_model_service
        from config import get_config
        
        # These should work without errors
        config = get_config()
        service = get_model_service()
        
        print("✅ Caching imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Caching test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Athena Improvements Test Suite")
    print("=" * 50)
    
    tests = [
        test_configuration,
        test_model_service,
        test_error_handling,
        test_caching
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {str(e)}")
            print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Improvements are working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit(main()) 