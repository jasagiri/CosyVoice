"""
CosyVoice3 WebUI Launcher
- Automatically finds an available port starting from 7865
- Launches the WebUI with the selected port
"""

import socket
import subprocess
import sys
import webbrowser
import time
import os

def is_port_available(port: int) -> bool:
    """Check if a port is available by trying to bind AND connect."""
    # First check if we can bind
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
    except (socket.error, OSError):
        return False
    
    # Also check if something is listening
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                return False  # Something is listening
    except:
        pass
    
    return True

def find_available_port(start_port: int = 7865, max_attempts: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    raise RuntimeError(f"No available port found in range {start_port}-{start_port + max_attempts}")

def main():
    model_dir = "pretrained_models/Fun-CosyVoice3-0.5B-2512"
    
    # Find available port
    print("Checking for available port...")
    try:
        port = find_available_port(7865)
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1
    
    if port != 7865:
        print(f"Port 7865 is in use. Using port {port} instead.")
    else:
        print(f"Using port {port}")
    
    print()
    print("=" * 50)
    print(f"  Starting CosyVoice3 WebUI")
    print(f"  URL: http://localhost:{port}")
    print("=" * 50)
    print()
    print("Press Ctrl+C to stop the server.")
    print()
    
    # Set environment variable for Gradio
    os.environ['GRADIO_SERVER_PORT'] = str(port)
    
    # Open browser after a delay
    def open_browser():
        time.sleep(8)
        webbrowser.open(f"http://localhost:{port}")
    
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Launch webui.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    webui_path = os.path.join(script_dir, "webui.py")
    
    try:
        subprocess.run([
            sys.executable,
            webui_path,
            "--port", str(port),
            "--model_dir", model_dir
        ], env=os.environ)
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
