import signal
import traceback
import sys
import os

def signal_handler(signum, frame):
    """Handle illegal instruction signal and capture stack trace"""
    print(f"Caught signal {signum} (SIGILL - Illegal Instruction)")
    print("Stack trace:")
    traceback.print_stack(frame)
    print("\nFrame info:")
    print(f"Filename: {frame.f_code.co_filename}")
    print(f"Function: {frame.f_code.co_name}")
    print(f"Line number: {frame.f_lineno}")
    
    # Try to get more detailed info about the instruction
    try:
        import subprocess
        pid = os.getpid()
        print(f"\nProcess ID: {pid}")
        print("Use 'lldb -p {pid}' to attach debugger if still running")
    except:
        pass
    
    sys.exit(1)

# Register signal handler for illegal instruction
signal.signal(signal.SIGILL, signal_handler)

def test_central_data_controller():
    """Test function with instrumentation"""
    try:
        print("Importing required modules...")
        # Add your imports here
        
        print("Creating central_data_controller instance...")
        # Add your controller instantiation here
        
        print("About to call start_Recording()...")
        # self.central_data_controller.start_Recording()
        
    except Exception as e:
        print(f"Exception before illegal instruction: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_central_data_controller()
