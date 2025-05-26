#!/usr/bin/env python3
"""
Quick Package Script for Calc-Arcade
Simple, working version that just builds the executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🎮 Quick Calc-Arcade Packager")
    print("=" * 40)
    
    project_root = Path(__file__).parent.parent
    print(f"📁 Project root: {project_root}")
    
    # Clean previous builds
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("🧹 Cleaned dist directory")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("🧹 Cleaned build directory")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Build with PyInstaller using simple command
    print("\n🔨 Building executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",          # Single executable file
        "--windowed",        # No console window
        "--name", "calc-arcade",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=project_root, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        
        # Check if executable was created
        exe_path = dist_dir / "calc-arcade.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executable created: {exe_path}")
            print(f"💾 Size: {size_mb:.1f} MB")
            
            print("\n🎉 SUCCESS!")
            print(f"Your calculator executable is ready at:")
            print(f"   {exe_path}")
            print("\nYou can now:")
            print("1. Run the executable to test it")
            print("2. Share it with others")
            print("3. Create a zip file for distribution")
            
        else:
            print("❌ Executable not found after build")
            
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error output: {e.stderr}")

if __name__ == "__main__":
    main()