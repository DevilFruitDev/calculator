#!/usr/bin/env python3
"""
Cross-Platform Package Script for Calc-Arcade
Handles building, packaging, and distribution for Windows, macOS, and Linux
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path
import json
import zipfile


class CalcArcadePackager:
    """Cross-platform packaging system for Calc-Arcade calculator."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.version = self.get_version()
        self.system = platform.system().lower()
        
        # Platform-specific configurations
        self.configs = {
            "windows": {
                "executable_name": "calc-arcade.exe",
                "icon_file": "assets/icons/app_icon.ico",
                "installer_type": "nsis"  # or "wix"
            },
            "darwin": {  # macOS
                "executable_name": "Calc-Arcade.app",
                "icon_file": "assets/icons/app_icon.icns", 
                "bundle_id": "com.calcarcade.calculator"
            },
            "linux": {
                "executable_name": "calc-arcade",
                "icon_file": "assets/icons/app_icon.png",
                "desktop_file": True
            }
        }
        
        print(f"🎮 Calc-Arcade Packager v{self.version}")
        print(f"📱 Detected platform: {platform.system()} ({platform.machine()})")
        print(f"📁 Project root: {self.project_root}")
    
    def get_version(self):
        """Extract version from setup.py or __init__.py."""
        try:
            # Try to get version from setup.py
            setup_file = self.project_root / "setup.py"
            if setup_file.exists():
                with open(setup_file, 'r') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if 'version=' in line and '"' in line:
                            return line.split('"')[1]
            
            # Fallback to a default version
            return "1.0.0"
        except Exception as e:
            print(f"⚠️ Could not determine version: {e}")
            return "1.0.0"
    
    def clean_build_dirs(self):
        """Clean previous build artifacts."""
        print("\n🧹 Cleaning build directories...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir]
        for directory in dirs_to_clean:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"   Removed: {directory}")
        
        # Create fresh directories
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        print("   ✅ Clean build environment ready")
    
    def check_dependencies(self):
        """Check if required packaging tools are installed."""
        print("\n🔍 Checking dependencies...")
        
        required_packages = ['pyinstaller']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"   ❌ {package} (missing)")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            for package in missing_packages:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                 check=True, capture_output=True)
                    print(f"   ✅ Installed {package}")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Failed to install {package}: {e}")
                    return False
        
        return True
    
    def run_tests(self):
        """Run test suite before packaging."""
        print("\n🧪 Running test suite...")
        
        try:
            # Run the test suite
            test_runner = self.project_root / "tests" / "run_tests.py"
            if test_runner.exists():
                result = subprocess.run([sys.executable, str(test_runner)], 
                                      capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode == 0:
                    print("   ✅ All tests passed!")
                    return True
                else:
                    print("   ❌ Tests failed!")
                    print(f"   Output: {result.stdout}")
                    print(f"   Error: {result.stderr}")
                    return False
            else:
                print("   ⚠️ Test runner not found, skipping tests")
                return True
                
        except Exception as e:
            print(f"   ❌ Error running tests: {e}")
            return False
    
    def create_pyinstaller_spec(self):
        """Create PyInstaller spec file for consistent builds."""
        print("\n📝 Creating PyInstaller specification...")
        
        config = self.configs.get(self.system, self.configs["linux"])
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['{self.project_root}'],
    binaries=[],
    datas=[
        ('ui', 'ui'),
        ('utils', 'utils'),
        ('assets', 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{config["executable_name"].replace(".exe", "").replace(".app", "")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{config["icon_file"]}' if Path(self.project_root / config["icon_file"]).exists() else None,
)
'''
        
        # Add macOS app bundle configuration
        if self.system == "darwin":
            spec_content += f'''
app = BUNDLE(
    exe,
    name='{config["executable_name"]}',
    icon='{config["icon_file"]}',
    bundle_identifier='{config["bundle_id"]}',
    info_plist={{
        'NSHighResolutionCapable': 'True',
        'CFBundleDisplayName': 'Calc-Arcade',
        'CFBundleVersion': '{self.version}',
        'CFBundleShortVersionString': '{self.version}',
    }},
)
'''
        
        spec_file = self.project_root / "calc-arcade.spec"
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        
        print(f"   ✅ Created spec file: {spec_file}")
        return spec_file
    
    def build_executable(self):
        """Build executable using PyInstaller."""
        print("\n🔨 Building executable...")
        
        spec_file = self.create_pyinstaller_spec()
        
        try:
            # Run PyInstaller
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--clean",
                "--noconfirm", 
                str(spec_file)
            ]
            
            print(f"   Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("   ✅ Executable built successfully!")
                return True
            else:
                print("   ❌ Build failed!")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Build error: {e}")
            return False
    
    def create_installer_package(self):
        """Create platform-specific installer package."""
        print("\n📦 Creating installer package...")
        
        if self.system == "windows":
            return self.create_windows_package()
        elif self.system == "darwin":
            return self.create_macos_package()
        else:
            return self.create_linux_package()
    
    def create_windows_package(self):
        """Create Windows installer package."""
        print("   🪟 Creating Windows package...")
        
        # Create zip distribution
        zip_name = f"calc-arcade-v{self.version}-windows.zip"
        zip_path = self.dist_dir / zip_name
        
        dist_exe = self.dist_dir / "calc-arcade.exe"
        if not dist_exe.exists():
            print(f"   ❌ Executable not found: {dist_exe}")
            return False
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add executable
            zipf.write(dist_exe, "calc-arcade.exe")
            
            # Add documentation
            docs = ["README.md", "LICENSE.md"]
            for doc in docs:
                doc_path = self.project_root / doc
                if doc_path.exists():
                    zipf.write(doc_path, doc)
            
            # Add docs folder
            docs_dir = self.project_root / "docs"
            if docs_dir.exists():
                for doc_file in docs_dir.rglob("*.md"):
                    zipf.write(doc_file, f"docs/{doc_file.name}")
        
        print(f"   ✅ Windows package created: {zip_name}")
        return True
    
    def create_macos_package(self):
        """Create macOS app bundle and DMG."""
        print("   🍎 Creating macOS package...")
        
        app_bundle = self.dist_dir / "Calc-Arcade.app"
        if not app_bundle.exists():
            print(f"   ❌ App bundle not found: {app_bundle}")
            return False
        
        # Create DMG (if create-dmg is available)
        dmg_name = f"calc-arcade-v{self.version}-macos.dmg"
        dmg_path = self.dist_dir / dmg_name
        
        try:
            # Simple zip for now (DMG creation requires additional tools)
            zip_name = f"calc-arcade-v{self.version}-macos.zip"
            zip_path = self.dist_dir / zip_name
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add app bundle recursively
                for file_path in app_bundle.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(self.dist_dir)
                        zipf.write(file_path, arcname)
                
                # Add documentation
                docs = ["README.md", "LICENSE.md"]
                for doc in docs:
                    doc_path = self.project_root / doc
                    if doc_path.exists():
                        zipf.write(doc_path, doc)
            
            print(f"   ✅ macOS package created: {zip_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ macOS packaging error: {e}")
            return False
    
    def create_linux_package(self):
        """Create Linux package (AppImage or tarball)."""
        print("   🐧 Creating Linux package...")
        
        executable = self.dist_dir / "calc-arcade"
        if not executable.exists():
            print(f"   ❌ Executable not found: {executable}")
            return False
        
        # Create tarball
        tarball_name = f"calc-arcade-v{self.version}-linux.tar.gz"
        tarball_path = self.dist_dir / tarball_name
        
        try:
            import tarfile
            
            with tarfile.open(tarball_path, 'w:gz') as tar:
                # Add executable
                tar.add(executable, arcname="calc-arcade/calc-arcade")
                
                # Add documentation
                docs = ["README.md", "LICENSE.md"]
                for doc in docs:
                    doc_path = self.project_root / doc
                    if doc_path.exists():
                        tar.add(doc_path, arcname=f"calc-arcade/{doc}")
                
                # Add docs folder
                docs_dir = self.project_root / "docs"
                if docs_dir.exists():
                    for doc_file in docs_dir.rglob("*.md"):
                        tar.add(doc_file, arcname=f"calc-arcade/docs/{doc_file.name}")
                
                # Create desktop file
                self.create_desktop_file()
                desktop_file = self.build_dir / "calc-arcade.desktop"
                if desktop_file.exists():
                    tar.add(desktop_file, arcname="calc-arcade/calc-arcade.desktop")
            
            print(f"   ✅ Linux package created: {tarball_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ Linux packaging error: {e}")
            return False
    
    def create_desktop_file(self):
        """Create Linux desktop file."""
        desktop_content = f"""[Desktop Entry]
Name=Calc-Arcade
Comment=Retro Game Boy-style calculator with personality
Exec=calc-arcade
Icon=calc-arcade
Type=Application
Categories=Utility;Calculator;
StartupNotify=true
Version={self.version}
"""
        
        desktop_file = self.build_dir / "calc-arcade.desktop"
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
    
    def create_source_package(self):
        """Create source code distribution."""
        print("\n📄 Creating source package...")
        
        source_name = f"calc-arcade-v{self.version}-source.zip"
        source_path = self.dist_dir / source_name
        
        try:
            with zipfile.ZipFile(source_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Include source files
                source_patterns = [
                    "*.py", "ui/**/*.py", "utils/**/*.py", "tests/**/*.py",
                    "*.md", "*.txt", "docs/**/*.md", "assets/**/*"
                ]
                
                for pattern in source_patterns:
                    for file_path in self.project_root.glob(pattern):
                        if file_path.is_file() and not self.should_exclude(file_path):
                            arcname = file_path.relative_to(self.project_root)
                            zipf.write(file_path, arcname)
            
            print(f"   ✅ Source package created: {source_name}")
            return True
            
        except Exception as e:
            print(f"   ❌ Source packaging error: {e}")
            return False
    
    def should_exclude(self, file_path):
        """Check if file should be excluded from source package."""
        exclude_patterns = [
            "__pycache__", ".pyc", ".git", ".DS_Store", 
            "build", "dist", "*.spec", ".vscode", ".idea"
        ]
        
        path_str = str(file_path)
        return any(pattern in path_str for pattern in exclude_patterns)
    
    def generate_checksums(self):
        """Generate checksums for all packages."""
        print("\n🔐 Generating checksums...")
        
        import hashlib
        
        checksums = {}
        checksum_file = self.dist_dir / "checksums.txt"
        
        for file_path in self.dist_dir.glob("*.zip"):
            if file_path.name != "checksums.txt":
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                    checksums[file_path.name] = file_hash
                    print(f"   {file_path.name}: {file_hash[:16]}...")
        
        # Write checksums file
        with open(checksum_file, 'w') as f:
            f.write(f"# Calc-Arcade v{self.version} - Package Checksums\n")
            f.write(f"# Generated on {platform.system()} {platform.release()}\n\n")
            for filename, checksum in checksums.items():
                f.write(f"{checksum}  {filename}\n")
        
        print(f"   ✅ Checksums saved to: checksums.txt")
    
    def create_release_info(self):
        """Create release information file."""
        print("\n📋 Creating release information...")
        
        release_info = {
            "version": self.version,
            "build_platform": platform.system(),
            "build_date": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()),
            "python_version": platform.python_version(),
            "packages": []
        }
        
        # List all created packages
        for file_path in self.dist_dir.glob("*.zip"):
            if file_path.name != "checksums.txt":
                release_info["packages"].append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "platform": self.extract_platform_from_filename(file_path.name)
                })
        
        # Save release info
        release_file = self.dist_dir / "release_info.json"
        with open(release_file, 'w') as f:
            json.dump(release_info, f, indent=2)
        
        print(f"   ✅ Release info saved to: release_info.json")
    
    def extract_platform_from_filename(self, filename):
        """Extract platform from package filename."""
        if "windows" in filename:
            return "Windows"
        elif "macos" in filename:
            return "macOS"
        elif "linux" in filename:
            return "Linux"
        elif "source" in filename:
            return "Source Code"
        else:
            return "Unknown"
    
    def print_summary(self):
        """Print packaging summary."""
        print("\n" + "="*60)
        print("🎉 PACKAGING COMPLETE!")
        print("="*60)
        
        print(f"📦 Version: {self.version}")
        print(f"📁 Output directory: {self.dist_dir}")
        print(f"📊 Packages created:")
        
        total_size = 0
        for file_path in self.dist_dir.glob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                size = file_path.stat().st_size
                total_size += size
                size_mb = size / (1024 * 1024)
                print(f"   📄 {file_path.name} ({size_mb:.1f} MB)")
        
        print(f"\n💾 Total size: {total_size / (1024 * 1024):.1f} MB")
        print(f"🎯 Ready for distribution!")
        print("="*60)
    
    def package(self, skip_tests=False, source_only=False):
        """Main packaging workflow."""
        print(f"🚀 Starting packaging workflow...")
        
        # Step 1: Clean build environment
        self.clean_build_dirs()
        
        # Step 2: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed!")
            return False
        
        # Step 3: Run tests (unless skipped)
        if not skip_tests:
            if not self.run_tests():
                print("❌ Tests failed! Use --skip-tests to bypass.")
                return False
        
        # Step 4: Create source package
        if not self.create_source_package():
            print("❌ Source packaging failed!")
            return False
        
        # Step 5: Build executable (unless source-only)
        if not source_only:
            if not self.build_executable():
                print("❌ Executable build failed!")
                return False
            
            # Step 6: Create installer package
            if not self.create_installer_package():
                print("❌ Installer packaging failed!")
                return False
        
        # Step 7: Generate checksums
        self.generate_checksums()
        
        # Step 8: Create release info
        self.create_release_info()
        
        # Step 9: Print summary
        self.print_summary()
        
        return True


def main():
    """Main entry point for the packaging script."""
    parser = argparse.ArgumentParser(description="Calc-Arcade Cross-Platform Packager")
    parser.add_argument("--skip-tests", action="store_true", 
                       help="Skip running tests before packaging")
    parser.add_argument("--source-only", action="store_true",
                       help="Create only source package (no executable)")
    parser.add_argument("--clean", action="store_true",
                       help="Clean build directories and exit")
    
    args = parser.parse_args()
    
    packager = CalcArcadePackager()
    
    if args.clean:
        packager.clean_build_dirs()
        print("🧹 Build directories cleaned!")
        return
    
    try:
        success = packager.package(skip_tests=args.skip_tests, source_only=args.source_only)
        if success:
            print("\n🎊 Packaging completed successfully!")
            sys.exit(0)
        else:
            print("\n💥 Packaging failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Packaging interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()