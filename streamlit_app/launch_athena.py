#!/usr/bin/env python3
"""
🚀 Athena Streamlit App Launcher
Easy deployment script for hackathon demos
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'plotly', 
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'lightgbm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("\n🎉 All dependencies are installed!")
    return True

def check_models():
    """Check if Athena models are available"""
    models_dir = Path(__file__).parent.parent / "models"
    
    required_models = [
        "athena_ensemble_model.pkl",
        "athena_xgb_model.pkl", 
        "athena_lgb_model.pkl",
        "athena_robust_scaler.pkl",
        "athena_advanced_encoders.pkl"
    ]
    
    missing_models = []
    
    for model_file in required_models:
        model_path = models_dir / model_file
        if model_path.exists():
            print(f"✅ {model_file}")
        else:
            missing_models.append(model_file)
            print(f"❌ {model_file}")
    
    if missing_models:
        print(f"\n⚠️  Missing models: {', '.join(missing_models)}")
        print("Please train the Athena models first!")
        return False
    
    print("\n🤖 All models are available!")
    return True

def launch_app(port=8501, open_browser=True):
    """Launch the Streamlit application"""
    print(f"\n🚀 Launching Athena on port {port}...")
    
    # Change to the streamlit_app directory
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # Build the command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "🏠_Home.py",
        "--server.port", str(port),
        "--server.headless", "false" if open_browser else "true"
    ]
    
    try:
        # Launch Streamlit
        print(f"📝 Command: {' '.join(cmd)}")
        print(f"🌐 URL: http://localhost:{port}")
        print(f"📁 Directory: {app_dir}")
        print("\n🎯 Press Ctrl+C to stop the application")
        print("="*50)
        
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n\n👋 Athena application stopped!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 ATHENA STREAMLIT LAUNCHER - ENHANCED EDITION")
    print("="*50)
    print("✨ With Advanced Animations & Polish")
    print("🎨 Hackathon-Ready Interactive Experience")
    print("="*50)
    
    # Check dependencies
    print("\n📦 Checking Dependencies...")
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first!")
        return 1
    
    # Check models
    print("\n🤖 Checking Models...")
    if not check_models():
        print("\n❌ Please train Athena models first!")
        print("Run: python scripts/advanced_model_training.py")
        return 1
    
    # Get port from command line or use default
    port = 8501
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  Invalid port number: {sys.argv[1]}")
            print("Using default port 8501")
    
    # Launch the application
    success = launch_app(port)
    
    if success:
        print("\n🎉 Athena launched successfully!")
        return 0
    else:
        print("\n❌ Failed to launch Athena!")
        return 1

if __name__ == "__main__":
    exit(main())