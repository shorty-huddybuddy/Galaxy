# capture_video.py
# Simple webcam capture using OpenCV
# Press ESC to exit

import cv2
import time

def main():
    cap = cv2.VideoCapture(0)  # 0 is default camera; change index if you have multiple

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    prev_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Warning: empty frame received")
            break

        # flip horizontally for mirror view (optional)
        frame = cv2.flip(frame, 1)

        # calculate FPS for display
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time) if curr_time != prev_time else 0.0
        prev_time = curr_time

        # Put FPS text on frame
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        cv2.imshow("Live Webcam - Press ESC to quit", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
