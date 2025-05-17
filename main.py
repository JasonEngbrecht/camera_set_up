#!/usr/bin/env python3
"""
Raspberry Pi Camera Viewer and Frame Capture using OpenCV

This program opens a video stream from the Raspberry Pi camera using OpenCV,
displays it in a window, and allows the user to:
- Capture frames by pressing the spacebar
- Exit the program by pressing 'q'

Captured frames are saved in the 'frames' folder with timestamped filenames.
"""

import cv2
import time
import os
from datetime import datetime

def main():
    # Create the frames directory if it doesn't exist
    frames_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Initialize the camera using OpenCV's VideoCapture
    # For Raspberry Pi camera, we use the Video4Linux2 (V4L2) interface
    # The camera is usually device 0
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Set camera properties (resolution)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Camera started successfully")
    print("Displaying video stream. Press SPACEBAR to capture a frame, 'q' to quit.")
    
    frame_count = 0
    
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Display live feed
        cv2.imshow("Raspberry Pi Camera", frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Exiting...")
            break
        elif key == ord(' '):  # spacebar
            # Generate a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"frame_{timestamp}_{frame_count}.jpg"
            filepath = os.path.join(frames_dir, filename)
            
            # Save the frame
            cv2.imwrite(filepath, frame)
            frame_count += 1
            print(f"Frame captured: {filename}")
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    print(f"Program ended. {frame_count} frames captured.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()
