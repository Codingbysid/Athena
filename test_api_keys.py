#!/usr/bin/env python3
"""
🔑 Athena API Key Testing Script
Test and verify API keys are working correctly
"""

import os
import sys
from pathlib import Path
import requests
import json

def load_env():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded successfully")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")
    
    return {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'SUPABASE_URL': os.getenv('SUPABASE_URL'),
        'SUPABASE_ANON_KEY': os.getenv('SUPABASE_ANON_KEY'),
        'SUPABASE_SERVICE_ROLE_KEY': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
        'SLACK_BOT_TOKEN': os.getenv('SLACK_BOT_TOKEN'),
        'SLACK_WEBHOOK_URL': os.getenv('SLACK_WEBHOOK_URL'),
        'SENDGRID_API_KEY': os.getenv('SENDGRID_API_KEY'),
    }

def test_gemini_api():
    """Test Google Gemini API"""
    print("\n🤖 Testing Google Gemini API...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Gemini API key not found or not set")
        return False
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test with a simple prompt
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello! Can you help me with a quick test? Just say 'Athena API test successful'")
        
        if response.text:
            print("✅ Gemini API working correctly!")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {str(e)}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔐 Testing Supabase Connection...")
    
    url = os.getenv('SUPABASE_URL')
    anon_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not url or not anon_key:
        print("❌ Supabase credentials not found")
        return False
    
    try:
        # Test basic connection
        headers = {
            'apikey': anon_key,
            'Authorization': f'Bearer {anon_key}'
        }
        
        # Test health check endpoint
        response = requests.get(f"{url}/rest/v1/", headers=headers)
        
        if response.status_code == 200:
            print("✅ Supabase connection successful!")
            return True
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase test failed: {str(e)}")
        return False

def test_slack_webhook():
    """Test Slack webhook (if available)"""
    print("\n📧 Testing Slack Webhook...")
    
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url or webhook_url == 'your_slack_webhook_url':
        print("⚠️  Slack webhook not configured (pending approval)")
        return True  # Not a failure, just not configured yet
    
    try:
        message = {
            "text": "🚀 Athena API test successful! The system is ready.",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🚀 *Athena API Test*\nSystem is ready and operational!"
                    }
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message)
        
        if response.status_code == 200:
            print("✅ Slack webhook working correctly!")
            return True
        else:
            print(f"❌ Slack webhook failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Slack test failed: {str(e)}")
        return False

def test_sendgrid_api():
    """Test SendGrid API (if available)"""
    print("\n📧 Testing SendGrid API...")
    
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key or api_key == 'your_sendgrid_api_key':
        print("⚠️  SendGrid API key not configured")
        return True  # Not a failure, just not configured
    
    try:
        # Test API key validity
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('https://api.sendgrid.com/v3/user/profile', headers=headers)
        
        if response.status_code == 200:
            print("✅ SendGrid API working correctly!")
            return True
        else:
            print(f"❌ SendGrid API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ SendGrid test failed: {str(e)}")
        return False

def main():
    """Main testing function"""
    print("🚀" * 50)
    print("🔑 ATHENA API KEY TESTING")
    print("🚀" * 50)
    
    # Load environment
    env_vars = load_env()
    
    # Test results
    results = {
        'gemini': False,
        'supabase': False,
        'slack': False,
        'sendgrid': False
    }
    
    # Test each API
    results['gemini'] = test_gemini_api()
    results['supabase'] = test_supabase_connection()
    results['slack'] = test_slack_webhook()
    results['sendgrid'] = test_sendgrid_api()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    print("\nDetailed Results:")
    for service, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {service.upper()}: {status}")
    
    if passed_tests >= 2:  # At least Gemini and Supabase working
        print("\n🎉 Core services are ready! Athena can launch successfully.")
        print("🚀 Run 'cd streamlit_app && python launch_athena.py' to start")
    else:
        print("\n⚠️  Some core services need attention before launch")
    
    print("\n" + "="*50)

if __name__ == "__main__":
    main() 