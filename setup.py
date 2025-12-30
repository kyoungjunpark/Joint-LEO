#!/usr/bin/env python3
"""
Setup script for Joint-LEO project
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        sys.exit(1)

def verify_installation():
    """Verify that key packages are installed"""
    print("\nVerifying installation...")
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__} installed")
        
        import numpy as np
        print(f"✓ NumPy {np.__version__} installed")
        
        import matplotlib
        print(f"✓ Matplotlib {matplotlib.__version__} installed")
        
        print("\n✓ All dependencies verified successfully!")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    dirs = [
        "results",
        "logs",
        "checkpoints"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Created {d}/")

def main():
    print("=" * 60)
    print("Joint-LEO Setup")
    print("=" * 60)
    
    check_python_version()
    install_requirements()
    verify_installation()
    create_directories()
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Navigate to src/models/rl_multi_bw_share/")
    print("2. Run: python train_pensieve.py --user 1")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
