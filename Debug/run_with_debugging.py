import os
import sys
import subprocess

def get_poetry_python():
    """Get the Python executable from Poetry's virtual environment"""
    try:
        result = subprocess.run(['poetry', 'env', 'info', '--path'], 
                              capture_output=True, text=True, check=True)
        venv_path = result.stdout.strip()
        python_path = os.path.join(venv_path, 'bin', 'python')
        if os.path.exists(python_path):
            return python_path
        # Fallback for Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        if os.path.exists(python_path):
            return python_path
    except subprocess.CalledProcessError:
        print("Warning: Could not get Poetry Python path, using system Python")
        return sys.executable
    
    return sys.executable

def run_with_lldb():
    """Run the main script under LLDB to catch the illegal instruction"""
    python_path = get_poetry_python()
    script_path = "User_Interface/Main_App.py"
    
    print("Starting LLDB session with Poetry's Python...")
    print(f"Python path: {python_path}")
    print("LLDB will automatically run the program and catch any illegal instructions...")
    
    # Create a temporary LLDB command file
    lldb_commands = """settings set -- target.run-args "User_Interface/Main_App.py"
run
continue
"""
    
    with open('/tmp/lldb_commands.txt', 'w') as f:
        f.write(lldb_commands)
    
    try:
        subprocess.run([
            'lldb',
            '--source', '/tmp/lldb_commands.txt',
            python_path
        ])
    finally:
        # Clean up the temporary file
        if os.path.exists('/tmp/lldb_commands.txt'):
            os.remove('/tmp/lldb_commands.txt')

def run_with_env_debugging():
    """Run with environment variables for debugging using Poetry"""
    env = os.environ.copy()
    
    # Enable various debugging options
    env['PYTHONFAULTHANDLER'] = '1'
    env['PYTHONDEVMODE'] = '1'
    env['MALLOC_CHECK_'] = '2'
    
    # NumPy debugging (if using NumPy)
    env['NPY_DISABLE_CPU_FEATURES'] = 'AVX2,AVX512F'
    
    # Run with Poetry to ensure proper environment
    subprocess.run(['poetry', 'run', 'python', 'User_Interface/Main_App.py'], env=env)

def run_with_poetry_debug():
    """Run with Poetry's built-in debugging and verbose output"""
    env = os.environ.copy()
    env['PYTHONFAULTHANDLER'] = '1'
    env['PYTHONVERBOSE'] = '1'
    
    # Use Poetry run with debugging enabled
    subprocess.run(['poetry', 'run', 'python', '-X', 'dev', 'User_Interface/Main_App.py'], env=env)

def run_with_env_debugging_simple():
    """Simple debugging run - try this first"""
    env = os.environ.copy()
    env['NPY_DISABLE_CPU_FEATURES'] = 'AVX2,AVX512F'
    env['PYTHONFAULTHANDLER'] = '1'
    
    print("Running with CPU feature limitations (most common fix)...")
    subprocess.run(['poetry', 'run', 'python', 'User_Interface/Main_App.py'], env=env)

if __name__ == "__main__":
    print("Choose debugging method:")
    print("1. Run with LLDB (recommended for illegal instruction)")
    print("2. Run with environment debugging")
    print("3. Run with Poetry verbose debugging")
    print("4. Simple CPU feature fix (try this first!)")
    
    choice = input("Enter choice (1, 2, 3, or 4): ")
    
    if choice == "1":
        run_with_lldb()
    elif choice == "2":
        run_with_env_debugging()
    elif choice == "3":
        run_with_poetry_debug()
    elif choice == "4":
        run_with_env_debugging_simple()
    else:
        print("Invalid choice")
