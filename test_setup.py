#!/usr/bin/env python3
"""
Quick setup verification script for Token-Diet Agent
Run this before demos to ensure everything works
"""

import sys
import os

def check_python_version():
    """Verify Python version is 3.10+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Verify all required packages are installed"""
    required = [
        "streamlit",
        "plotly", 
        "langgraph",
        "chromadb",
        "langchain_groq",
        "langchain_huggingface",
        "pypdf",
        "tiktoken",
        "dotenv"
    ]
    
    missing = []
    for package in required:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Install missing packages:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Verify .env file exists and has GROQ_API_KEY"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("\n📝 Create .env file with:")
        print("GROQ_API_KEY=your_api_key_here")
        return False
    
    print("✅ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not set in .env")
        return False
    
    if api_key.startswith("gsk_"):
        print(f"✅ GROQ_API_KEY configured (starts with gsk_)")
    else:
        print("⚠️  GROQ_API_KEY format looks unusual (should start with gsk_)")
    
    return True

def check_sample_document():
    """Verify sample document exists"""
    if not os.path.exists("sample_document.txt"):
        print("⚠️  sample_document.txt not found (optional)")
        return True
    
    print("✅ sample_document.txt exists")
    return True

def check_project_structure():
    """Verify key files and folders exist"""
    required_paths = [
        "app/agents/graph.py",
        "app/services/router.py",
        "app/services/pruner.py",
        "app/services/judge.py",
        "app/utils/file_loader.py",
        "ui.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for path in required_paths:
        if os.path.exists(path):
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test that core modules can be imported"""
    try:
        from app.agents.graph import build_agent_graph
        print("✅ Agent graph imports successfully")
        
        from app.services.router import ModelRouter
        print("✅ Router imports successfully")
        
        from app.services.pruner import SemanticPruner
        print("✅ Pruner imports successfully")
        
        from app.services.judge import ResponseJudge
        print("✅ Judge imports successfully")
        
        from app.utils import count_tokens
        print("✅ Utils import successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Token-Diet Agent - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Project Structure", check_project_structure),
        ("Sample Document", check_sample_document),
        ("Module Imports", test_imports)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        print("-" * 60)
        result = check_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run:")
        print("\n   streamlit run ui.py")
        print("\n💡 For demo preparation, see DEMO_CHECKLIST.md")
        return 0
    else:
        print("\n⚠️  Some checks failed. Fix the issues above and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
