"""
Diagnostic script to test the gesture detection system
Run this to check if everything is working correctly
"""

import sys
import importlib.util

print("=" * 60)
print("GESTURE DETECTION SYSTEM - DIAGNOSTIC CHECK")
print("=" * 60)

# Check Python version
print(f"\n✓ Python Version: {sys.version}")

# Check required packages
packages = {
    'cv2': 'opencv-python',
    'mediapipe': 'mediapipe',
    'flask': 'flask',
    'flask_socketio': 'flask-socketio',
    'eventlet': 'eventlet'
}

print("\n📦 Checking required packages:")
all_installed = True
for module_name, package_name in packages.items():
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"  ❌ {package_name} - NOT INSTALLED")
        all_installed = False
    else:
        try:
            mod = importlib.import_module(module_name)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✓ {package_name} - version {version}")
        except Exception as e:
            print(f"  ⚠️ {package_name} - installed but error: {e}")

# Check webcam
print("\n📷 Checking webcam:")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ Webcam working - Resolution: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("  ⚠️ Webcam opened but can't read frames")
        cap.release()
    else:
        print("  ❌ Cannot open webcam")
except Exception as e:
    print(f"  ❌ Webcam error: {e}")

# Check port availability
print("\n🔌 Checking port 5000:")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 5000))
    sock.close()
    if result == 0:
        print("  ⚠️ Port 5000 is already in use")
    else:
        print("  ✓ Port 5000 is available")
except Exception as e:
    print(f"  ❌ Error checking port: {e}")

print("\n" + "=" * 60)
if all_installed:
    print("✅ All checks passed! You can run the server.")
    print("\nTo start the server, run:")
    print("  python backend\\gesture_server.py")
else:
    print("❌ Some packages are missing. Install them with:")
    print("  pip install -r requirements.txt")
print("=" * 60)
