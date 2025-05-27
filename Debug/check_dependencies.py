import subprocess
import sys
import importlib
import os

def check_binary_architecture(module_name):
    """Check the architecture of compiled extensions in a module"""
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__file__') and module.__file__:
            module_dir = os.path.dirname(module.__file__)
            
            # Find .so files (compiled extensions)
            for root, dirs, files in os.walk(module_dir):
                for file in files:
                    if file.endswith('.so') or file.endswith('.dylib'):
                        filepath = os.path.join(root, file)
                        try:
                            result = subprocess.run(['file', filepath], 
                                                 capture_output=True, text=True)
                            print(f"{filepath}: {result.stdout.strip()}")
                            
                            # Check with otool for more details
                            otool_result = subprocess.run(['otool', '-h', filepath], 
                                                        capture_output=True, text=True)
                            if otool_result.returncode == 0:
                                print(f"  Architecture details: {otool_result.stdout}")
                        except Exception as e:
                            print(f"  Error checking {filepath}: {e}")
                            
    except ImportError:
        print(f"Could not import {module_name}")
    except Exception as e:
        print(f"Error checking {module_name}: {e}")

def main():
    print("Checking Python executable architecture:")
    result = subprocess.run(['file', sys.executable], capture_output=True, text=True)
    print(f"Python: {result.stdout.strip()}")
    
    print(f"\nPython version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Check common packages that might have compiled extensions
    packages_to_check = [
        'numpy',
        'scipy',
        'pandas',
        'matplotlib',
        'sklearn',
        'tensorflow',
        'torch',
        'cv2',  # OpenCV
        # Add any other packages your central_data_controller might use
    ]
    
    print("\nChecking package architectures:")
    for package in packages_to_check:
        print(f"\n--- {package} ---")
        check_binary_architecture(package)

if __name__ == "__main__":
    main()
