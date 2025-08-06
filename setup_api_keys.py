#!/usr/bin/env python3
"""
🔑 Athena API Key Setup Script
Interactive script to help you configure API keys for Athena
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print the setup banner"""
    print("🚀" * 50)
    print("🔑 ATHENA API KEY SETUP")
    print("🚀" * 50)
    print()

def get_api_key_info():
    """Display information about required API keys"""
    print("📋 REQUIRED API KEYS:")
    print()
    print("🤖 AI Services:")
    print("  • Google Gemini API - For AI diagnostics and insights")
    print("    → Get at: https://makersuite.google.com/app/apikey")
    print()
    print("🏢 Salesforce Integration:")
    print("  • Salesforce Connected App credentials")
    print("    → Get at: https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm")
    print()
    print("🔐 Authentication (Optional):")
    print("  • Supabase - For user authentication")
    print("    → Get at: https://supabase.com/")
    print()
    print("📧 Communication (Optional):")
    print("  • Slack - For notifications")
    print("    → Get at: https://api.slack.com/apps")
    print("  • SendGrid - For email notifications")
    print("    → Get at: https://sendgrid.com/")
    print()

def interactive_setup():
    """Interactive API key setup"""
    print("🎯 Let's set up your API keys interactively!")
    print("(Press Enter to skip any key you don't have yet)")
    print()
    
    env_content = []
    
    # AI Services
    print("🤖 AI SERVICES:")
    gemini_key = input("Google Gemini API Key: ").strip()
    if gemini_key:
        env_content.append(f"GEMINI_API_KEY={gemini_key}")
    else:
        env_content.append("GEMINI_API_KEY=your_gemini_api_key_here")
    
    print()
    
    # Salesforce
    print("🏢 SALESFORCE INTEGRATION:")
    sf_client_id = input("Salesforce Client ID: ").strip()
    sf_client_secret = input("Salesforce Client Secret: ").strip()
    sf_username = input("Salesforce Username: ").strip()
    sf_password = input("Salesforce Password: ").strip()
    sf_token = input("Salesforce Security Token: ").strip()
    sf_instance = input("Salesforce Instance URL: ").strip()
    
    if sf_client_id:
        env_content.extend([
            f"SALESFORCE_CLIENT_ID={sf_client_id}",
            f"SALESFORCE_CLIENT_SECRET={sf_client_secret}",
            f"SALESFORCE_USERNAME={sf_username}",
            f"SALESFORCE_PASSWORD={sf_password}",
            f"SALESFORCE_SECURITY_TOKEN={sf_token}",
            f"SALESFORCE_INSTANCE_URL={sf_instance}"
        ])
    else:
        env_content.extend([
            "SALESFORCE_CLIENT_ID=your_salesforce_client_id",
            "SALESFORCE_CLIENT_SECRET=your_salesforce_client_secret",
            "SALESFORCE_USERNAME=your_salesforce_username",
            "SALESFORCE_PASSWORD=your_salesforce_password",
            "SALESFORCE_SECURITY_TOKEN=your_salesforce_security_token",
            "SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com"
        ])
    
    print()
    
    # Supabase
    print("🔐 SUPABASE AUTHENTICATION:")
    supabase_url = input("Supabase URL: ").strip()
    supabase_anon = input("Supabase Anon Key: ").strip()
    supabase_service = input("Supabase Service Role Key: ").strip()
    
    if supabase_url:
        env_content.extend([
            f"SUPABASE_URL={supabase_url}",
            f"SUPABASE_ANON_KEY={supabase_anon}",
            f"SUPABASE_SERVICE_ROLE_KEY={supabase_service}"
        ])
    else:
        env_content.extend([
            "SUPABASE_URL=https://your-project.supabase.co",
            "SUPABASE_ANON_KEY=your_supabase_anon_key",
            "SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key"
        ])
    
    print()
    
    # Communication
    print("📧 COMMUNICATION SERVICES:")
    slack_token = input("Slack Bot Token: ").strip()
    slack_webhook = input("Slack Webhook URL: ").strip()
    sendgrid_key = input("SendGrid API Key: ").strip()
    
    if slack_token:
        env_content.extend([
            f"SLACK_BOT_TOKEN={slack_token}",
            f"SLACK_WEBHOOK_URL={slack_webhook}"
        ])
    else:
        env_content.extend([
            "SLACK_BOT_TOKEN=your_slack_bot_token",
            "SLACK_WEBHOOK_URL=your_slack_webhook_url"
        ])
    
    if sendgrid_key:
        env_content.append(f"SENDGRID_API_KEY={sendgrid_key}")
    else:
        env_content.append("SENDGRID_API_KEY=your_sendgrid_api_key")
    
    # Feature flags
    env_content.extend([
        "",
        "# Feature Flags",
        "ENABLE_GEMINI_AI=true",
        "ENABLE_SALESFORCE_INTEGRATION=true",
        "ENABLE_SUPABASE_AUTH=false",
        "ENABLE_SLACK_NOTIFICATIONS=true",
        "ENABLE_EMAIL_NOTIFICATIONS=false",
        "ENABLE_MONITORING=true",
        "ENABLE_ANALYTICS=true",
        "ENABLE_ANIMATIONS=true"
    ])
    
    return env_content

def write_env_file(env_content):
    """Write the .env file"""
    env_path = Path(".env")
    
    # Add header
    header = [
        "# 🚀 Athena - Environment Configuration",
        "# Generated by setup_api_keys.py",
        ""
    ]
    
    full_content = header + env_content
    
    with open(env_path, 'w') as f:
        f.write('\n'.join(full_content))
    
    print(f"✅ Created {env_path}")
    print(f"📝 Total configuration lines: {len(full_content)}")

def main():
    """Main setup function"""
    print_banner()
    get_api_key_info()
    
    response = input("🎯 Would you like to set up your API keys now? (y/n): ").lower()
    
    if response in ['y', 'yes']:
        print()
        env_content = interactive_setup()
        write_env_file(env_content)
        print()
        print("🎉 Setup complete!")
        print("📝 Edit .env file to add more keys as needed")
        print("🚀 Run 'cd streamlit_app && python launch_athena.py' to start Athena")
    else:
        print()
        print("📝 You can manually edit the .env file with your API keys")
        print("📖 See .env.example for all available options")

if __name__ == "__main__":
    main() 