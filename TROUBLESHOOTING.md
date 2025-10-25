# 🔧 TROUBLESHOOTING GUIDE

## Issues Fixed:

### 1. ✅ Model Loading Issue
**Problem:** HORNET.glb not loading
**Solution:** 
- Changed path from `'../HORNET.glb'` to `'/HORNET.glb'`
- Updated Flask static folder configuration to serve files from root directory
- Added console logging to debug model loading

### 2. ✅ Connection Issue  
**Problem:** Socket.IO not connecting or gesture data not updating
**Solutions:**
- Added proper Socket.IO configuration with reconnection settings
- Set async_mode to 'threading' in Flask-SocketIO
- Added connection error handling
- Made gesture data emit continuously (not just when hands detected)
- Added detailed console logging

## How to Test:

### Step 1: Stop any running servers
Press `Ctrl+C` in the terminal running the server

### Step 2: Restart the server
```powershell
cd C:\Users\Dinesh\Project\Galaxy
python backend\gesture_server.py
```

### Step 3: Open browser and check console
1. Navigate to `http://localhost:5000`
2. Press `F12` to open Developer Tools
3. Go to "Console" tab
4. You should see:
   - "Initializing Socket.IO connection..."
   - "✅ Connected to gesture server - Socket ID: xxx"
   - "Model loaded successfully!" or "Creating procedural solar system"
   - "Received gesture data: {zoom: 50, rotate_x: 0, rotate_y: 0}"

### Step 4: Verify gesture detection
1. Look at the webcam window (should open automatically)
2. Put your hands in front of the camera
3. Check the terminal output - should show gesture data being sent
4. Check the browser - statistics should update in real-time

## Debugging Checklist:

### ❓ Model not loading?
Check browser console for error message:
- If "404" error: Model file path is wrong
- If "CORS" error: Server static folder configuration issue
- **Current fix:** Model should now load from `/HORNET.glb`

### ❓ Connection status shows "Disconnected"?
1. Check if server is running: Open `http://localhost:5000/test`
   - Should show: "Server is running! Current gesture data: {...}"
   - If not loading: Server isn't running
2. Check browser console for error messages
3. Try refreshing the page (F5)
4. **Current fix:** Added proper Socket.IO configuration and error handling

### ❓ Gesture statistics not updating?
1. Check if webcam window is showing your hands
2. Look for green landmarks on your hands in webcam window
3. Check browser console - should see "Received gesture data" messages
4. Check terminal - should see gesture data being printed
5. **Current fix:** Server now emits data continuously

### ❓ Webcam not working?
1. Close all other apps using webcam (Zoom, Teams, etc.)
2. Try different camera index:
   - Edit `backend/gesture_server.py` line 100
   - Change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` or `2`
3. Grant camera permissions to Python

### ❓ Port 5000 already in use?
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

## Quick Test Commands:

### Test 1: Check if server responds
Open browser to: `http://localhost:5000/test`
Expected: "Server is running! Current gesture data: {..."

### Test 2: Check Socket.IO connection
Open browser console and type:
```javascript
socket.connected
```
Expected: `true`

### Test 3: Manually test gesture update
In browser console:
```javascript
socket.on('gesture_update', (data) => console.log('GOT DATA:', data));
```
Expected: Should see data logs appearing

## Common Error Messages:

### "Failed to load resource: net::ERR_CONNECTION_REFUSED"
- Server is not running
- Solution: Start server with `python backend\gesture_server.py`

### "CORS policy error"
- Fixed in updated code
- Server now allows all origins

### "Cannot read property of undefined"
- Socket.IO not initialized properly
- Fixed with proper error handling

### "THREE.GLTFLoader is not a constructor"  
- Fixed: Using correct Three.js loader imports

## Files Modified:

1. ✅ `backend/gesture_server.py`
   - Added threading async_mode
   - Fixed static folder path
   - Continuous gesture emission
   - Better logging

2. ✅ `frontend/main.js`  
   - Fixed model path: `/HORNET.glb`
   - Enhanced Socket.IO config
   - Added connection error handling
   - Added debug logging

3. ✅ Created `diagnostic.py`
   - Check all dependencies
   - Test webcam
   - Verify port availability

## Next Steps:

1. **Restart the server** (important!)
2. **Clear browser cache** (Ctrl+Shift+Delete)
3. **Reload the page** (F5 or Ctrl+F5)
4. **Watch the console** for debug messages
5. **Move your hands** in front of webcam

## Still Having Issues?

Check the terminal and browser console outputs and look for:
- Red error messages
- Connection status in top-left of webpage
- Gesture data values updating in real-time

The console logs will tell you exactly what's happening!
