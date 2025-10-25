# 🌌 Hand Gesture Controlled 3D Models

An interactive 3D solar system visualization controlled by hand gestures using computer vision and WebGL.

## 🎯 Features

- **Real-time Hand Gesture Detection**: Uses OpenCV and MediaPipe to detect hand gestures from webcam
- **Two-Hand Zoom Control**: Spread or pinch your index fingers to zoom in/out
- **One-Hand Rotation**: Move a single hand to rotate the solar system view
- **3D Visualization**: Beautiful Three.js rendered solar system with planets and orbits
- **Real-time Communication**: Flask-SocketIO for instant gesture data transmission
- **Smooth Animations**: Interpolated camera movements for smooth user experience

## 📁 Project Structure

```
Galaxy/
├── backend/
│   └── gesture_server.py      # Python gesture detection server
├── frontend/
│   ├── index.html             # Main HTML page
│   ├── main.js                # Three.js viewer logic
│   └── solar_system.glb       # 3D model (optional)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Install Python Dependencies

You already have a virtual environment at `handgasture`. Activate it and install dependencies:

**PowerShell:**
```powershell
.\handgasture\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Command Prompt:**
```cmd
.\handgasture\Scripts\activate.bat
pip install -r requirements.txt
```

### Step 2: (Optional) Add 3D Solar System Model

Place a `solar_system.glb` file in the `frontend/` directory for a custom 3D model. If not provided, a procedural solar system will be generated automatically.

You can find free solar system models at:
- [Sketchfab](https://sketchfab.com/search?q=solar+system&type=models)
- [NASA 3D Resources](https://nasa3d.arc.nasa.gov/)

## 🎮 Usage

### Start the Server

1. Activate your virtual environment:
   ```powershell
   .\handgasture\Scripts\Activate.ps1
   ```

2. Run the gesture server:
   ```powershell
   python backend\gesture_server.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Hand Gestures

- **Zoom Control (Two Hands)**: 
  - Extend both index fingers
  - Spread hands apart to zoom out
  - Bring hands together to zoom in

- **Rotation Control (One Hand)**:
  - Use a single hand to rotate the view
  - Move hand left/right for Y-axis rotation
  - Move hand up/down for X-axis rotation

### Tips for Best Results

- Ensure good lighting for hand detection
- Keep hands visible to the camera
- Position camera to capture both hands when zooming
- The webcam feed window shows detected hand landmarks
- Press 'q' in the webcam window to stop gesture detection

## 🛠️ Technical Details

### Backend (Python)

- **OpenCV**: Captures webcam feed
- **MediaPipe**: Detects hand landmarks in real-time
- **Flask**: Serves the web application
- **Flask-SocketIO**: Provides WebSocket communication

### Frontend (JavaScript)

- **Three.js**: 3D rendering engine
- **Socket.IO**: Receives real-time gesture data
- **GLTFLoader**: Loads 3D models
- **OrbitControls**: Camera control system

### Gesture Processing

1. MediaPipe detects up to 2 hands with 21 landmarks each
2. Index fingertips (landmark 8) calculate zoom distance
3. Wrist and finger positions calculate rotation angles
4. Data sent via WebSocket at ~30 FPS
5. Frontend applies smooth interpolation for natural movement

## 📊 Gesture Data Format

```javascript
{
    "zoom": 0-100,      // Zoom level percentage
    "rotate_x": -180 to 180,  // X-axis rotation in degrees
    "rotate_y": -180 to 180   // Y-axis rotation in degrees
}
```

## 🐛 Troubleshooting

### Webcam not detected
- Check if another application is using the camera
- Try changing camera index in `gesture_server.py` line 111:
  ```python
  cap = cv2.VideoCapture(0)  # Try 1, 2, etc.
  ```

### Hand detection not working
- Ensure good lighting conditions
- Adjust MediaPipe confidence in `gesture_server.py` lines 24-25:
  ```python
  min_detection_confidence=0.5,  # Lower for easier detection
  min_tracking_confidence=0.5
  ```

### Connection errors
- Ensure port 5000 is not in use
- Check firewall settings
- Verify Flask server is running

### Poor performance
- Close unnecessary applications
- Reduce camera resolution in `gesture_server.py` lines 112-113
- Adjust LERP_FACTOR in `main.js` line 14 for less smoothing

## 🎨 Customization

### Change Zoom Range
Edit `main.js` line 228:
```javascript
const targetDistance = THREE.MathUtils.lerp(5, 30, 1 - (targetZoom / 100));
// Change 5 (min) and 30 (max) to your preferred values
```

### Adjust Smoothing
Edit `main.js` line 14:
```javascript
const LERP_FACTOR = 0.1; // Lower = smoother, Higher = more responsive
```

### Modify Planet Colors/Sizes
Edit `solar_system.json` at the project root. Example fields:

```json
{
  "sun": { "radius": 1.0, "color": "#ffff00" },
  "planets": [
    { "name": "Earth", "distance": 4, "radius": 0.5, "color": "#4169e1" }
  ],
  "stars": { "count": 1000, "spread": 100, "size": 0.1 }
}
```
Colors accept CSS hex strings (e.g., "#ff4500"). Rings can be added via a `rings` object: `{ "innerScale": 1.3, "outerScale": 2.0, "color": "#c9b581", "opacity": 0.6 }`.

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Credits

- **MediaPipe**: Google's ML framework for hand tracking
- **Three.js**: 3D graphics library
- **Flask-SocketIO**: Real-time web communication

## 🚀 Future Enhancements

- [ ] Add more gesture controls (pinch, swipe, etc.)
- [ ] Include planet information overlays
- [ ] Add gesture training mode
- [ ] Multi-user support
- [ ] VR/AR integration
- [ ] Voice commands integration

---

**Enjoy exploring the solar system with your hands! 🌍✨**
