"""
Step 1: Test Environment Setup
This script checks that all packages are installed and API keys are loaded.
"""
import os
import sys

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 50)
print("VidGen Environment Test")
print("=" * 50)
print(f"Project folder: {SCRIPT_DIR}")
print(f"Python version: {sys.version}")

# Test 1: Check all imports work
print("\n1. Testing imports...")
try:
    import anthropic
    print("   [OK] anthropic")
except ImportError as e:
    print(f"   [FAIL] anthropic: {e}")

try:
    import replicate
    print("   [OK] replicate")
except ImportError as e:
    print(f"   [FAIL] replicate: {e}")

try:
    from PIL import Image
    print("   [OK] Pillow (PIL)")
except ImportError as e:
    print(f"   [FAIL] Pillow: {e}")

try:
    import cv2
    print("   [OK] opencv-python (cv2)")
except ImportError as e:
    print(f"   [FAIL] opencv: {e}")

try:
    from pydantic import BaseModel
    print("   [OK] pydantic")
except ImportError as e:
    print(f"   [FAIL] pydantic: {e}")

try:
    from dotenv import load_dotenv
    print("   [OK] python-dotenv")
except ImportError as e:
    print(f"   [FAIL] python-dotenv: {e}")

try:
    from rich import print as rprint
    print("   [OK] rich")
except ImportError as e:
    print(f"   [FAIL] rich: {e}")

# Test 2: Check .env file and API keys
print("\n2. Testing .env file...")
from dotenv import load_dotenv

# Load .env file from the project directory
env_path = os.path.join(SCRIPT_DIR, ".env")
print(f"   Looking for .env at: {env_path}")
load_dotenv(env_path, override=True)

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
replicate_token = os.getenv("REPLICATE_API_TOKEN")

if anthropic_key:
    # Show only first/last few chars for security
    masked = anthropic_key[:10] + "..." + anthropic_key[-4:]
    print(f"   [OK] ANTHROPIC_API_KEY found: {masked}")
else:
    print("   [FAIL] ANTHROPIC_API_KEY not found!")

if replicate_token:
    masked = replicate_token[:5] + "..." + replicate_token[-4:]
    print(f"   [OK] REPLICATE_API_TOKEN found: {masked}")
else:
    print("   [FAIL] REPLICATE_API_TOKEN not found!")

# Summary
print("\n" + "=" * 50)
if anthropic_key and replicate_token:
    print("SUCCESS! All checks passed. Environment is ready.")
else:
    print("Some checks failed. Please fix the issues above.")
print("=" * 50)
