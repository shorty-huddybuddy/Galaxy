"""
Hand Gesture Detection Server
Uses OpenCV and MediaPipe to detect hand gestures and send data to frontend via Flask-SocketIO
"""

import cv2
import mediapipe as mp
import math
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time

# Initialize Flask app and SocketIO
app = Flask(__name__, template_folder='../frontend', static_folder='..', static_url_path='')
app.config['SECRET_KEY'] = 'solar_system_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Global variables
gesture_data = {
    'zoom': 85,  # Default zoom level (0-100) - higher = closer
    'rotate_x': 0,  # Rotation around X axis
    'rotate_y': 0,  # Rotation around Y axis
}
running = False

ROT_SENSITIVITY_X = 90.0   # degrees for vertical (up/down)
ROT_SENSITIVITY_Y = 90.0   # degrees for horizontal (left/right)
ROT_SMOOTHING = 0.5        # 0-1, higher is more responsive


def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def calculate_angle(point1, point2):
    """Calculate angle between two points"""
    return math.atan2(point2.y - point1.y, point2.x - point1.x) * 180 / math.pi


def process_hand_gestures(results, frame_width, frame_height):
    """
    Process detected hands and extract gesture data
    Returns: Updated gesture data dictionary
    """
    global gesture_data
    
    if results.multi_hand_landmarks:
        num_hands = len(results.multi_hand_landmarks)
        
        if num_hands == 2:
            # Two hands detected - calculate zoom based on distance between index fingertips
            hand1 = results.multi_hand_landmarks[0]
            hand2 = results.multi_hand_landmarks[1]

            # Get index fingertip landmarks (landmark 8)
            index_tip1 = hand1.landmark[8]
            index_tip2 = hand2.landmark[8]

            # Calculate distance between fingertips
            distance = calculate_distance(index_tip1, index_tip2)

            # Map distance to zoom value (0-100)
            # Typical distance range: 0.05 to 0.8
            zoom_value = max(0, min(100, (distance - 0.05) * 133))
            gesture_data['zoom'] = zoom_value

        elif num_hands == 1:
            # Single hand detected - do NOT update zoom, keep last value
            # Single hand detected - map index finger movement to rotations
            hand = results.multi_hand_landmarks[0]

            # Landmarks
            wrist = hand.landmark[0]
            index_tip = hand.landmark[8]

            # Relative movement of index to wrist (normalized -1..1 approx)
            dx = index_tip.x - wrist.x  # left/right movement
            dy = index_tip.y - wrist.y  # up/down movement (note: y increases downward)

            # Direct mapping, less smoothing, moderate sensitivity
            gesture_data['rotate_y'] = dx * ROT_SENSITIVITY_Y
            gesture_data['rotate_x'] = -dy * ROT_SENSITIVITY_X
    
    return gesture_data


def gesture_detection_loop():
    """Main loop for detecting hand gestures from webcam"""
    global running, gesture_data
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Starting gesture detection... Press 'q' to quit")
    
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe
        results = hands.process(rgb_frame)
        
        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS
                )
            
            # Process gestures
            process_hand_gestures(results, frame.shape[1], frame.shape[0])
        
        # Emit gesture data to connected clients (always emit, not just when hands detected)
        socketio.emit('gesture_update', gesture_data, namespace='/')
        
        # Display gesture information on frame
        cv2.putText(frame, f"Zoom: {gesture_data['zoom']:.1f}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Rotate X: {gesture_data['rotate_x']:.1f}", 
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Rotate Y: {gesture_data['rotate_y']:.1f}", 
                    (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Two hands: Zoom | One hand: Rotate", 
                    (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Hand Gesture Detection', frame)
        
        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break
        
        time.sleep(0.03)  # ~30 FPS
    
    cap.release()
    cv2.destroyAllWindows()
    print("Gesture detection stopped")


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/test')
def test():
    """Test endpoint to verify server is running"""
    return f'Server is running! Current gesture data: {gesture_data}'


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('✅ Client connected!')
    # Send initial gesture data to newly connected client
    emit('gesture_update', gesture_data)
    print(f'Sent initial gesture data: {gesture_data}')


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('❌ Client disconnected')


@socketio.on('start_detection')
def handle_start_detection():
    """Start gesture detection when requested by client"""
    global running
    if not running:
        running = True
        detection_thread = threading.Thread(target=gesture_detection_loop)
        detection_thread.daemon = True
        detection_thread.start()
        print("Gesture detection started")


if __name__ == '__main__':
    print("="*50)
    print("Hand Gesture Controlled Solar System Server")
    print("="*50)
    print("Starting server on http://localhost:5000")
    print("Gesture detection will start automatically")
    print("="*50)
    
    # Start gesture detection in background
    running = True
    detection_thread = threading.Thread(target=gesture_detection_loop)
    detection_thread.daemon = True
    detection_thread.start()
    
    # Start Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
