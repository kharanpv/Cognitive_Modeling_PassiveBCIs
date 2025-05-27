import subprocess
import sys
import json
import os

def check_poetry_environment():
    """Check Poetry environment and Python architecture"""
    try:
        # Get Poetry environment info
        result = subprocess.run(['poetry', 'env', 'info'], capture_output=True, text=True)
        print("Poetry Environment Info:")
        print(result.stdout)
        
        # Get Poetry's Python path
        result = subprocess.run(['poetry', 'env', 'info', '--path'], 
                              capture_output=True, text=True, check=True)
        venv_path = result.stdout.strip()
        python_path = os.path.join(venv_path, 'bin', 'python')
        
        if not os.path.exists(python_path):
            python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        
        # Check Python architecture
        if os.path.exists(python_path):
            result = subprocess.run(['file', python_path], capture_output=True, text=True)
            print(f"\nPoetry Python Architecture: {result.stdout.strip()}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error checking Poetry environment: {e}")

def check_poetry_packages():
    """Check installed packages and their details"""
    try:
        # Get list of installed packages
        result = subprocess.run(['poetry', 'show'], capture_output=True, text=True)
        print("\nInstalled packages:")
        print(result.stdout)
        
        # Check specific packages that might have compiled extensions
        problematic_packages = ['numpy', 'pandas', 'pynput', 'opencv-python', 'pillow']
        
        for package in problematic_packages:
            try:
                result = subprocess.run(['poetry', 'show', package], 
                                      capture_output=True, text=True, check=True)
                print(f"\n--- {package} details ---")
                print(result.stdout)
            except subprocess.CalledProcessError:
                print(f"\n{package} not installed")
                
    except subprocess.CalledProcessError as e:
        print(f"Error checking packages: {e}")

def check_binary_architectures():
    """Check binary architectures of installed packages"""
    try:
        # Get site-packages directory
        result = subprocess.run(['poetry', 'run', 'python', '-c', 
                               'import site; print(site.getsitepackages()[0])'], 
                              capture_output=True, text=True, check=True)
        site_packages = result.stdout.strip()
        
        print(f"\nChecking binaries in: {site_packages}")
        
        # Look for .so files and .dylib files
        for root, dirs, files in os.walk(site_packages):
            for file in files:
                if file.endswith('.so') or file.endswith('.dylib'):
                    filepath = os.path.join(root, file)
                    try:
                        result = subprocess.run(['file', filepath], 
                                              capture_output=True, text=True)
                        arch_info = result.stdout.strip()
                        if 'x86_64' in arch_info or 'arm64' in arch_info:
                            print(f"{file}: {arch_info}")
                    except Exception:
                        pass
                        
    except subprocess.CalledProcessError as e:
        print(f"Error checking binaries: {e}")

if __name__ == "__main__":
    print("Checking Poetry environment and dependencies...")
    check_poetry_environment()
    check_poetry_packages()
    check_binary_architectures()
