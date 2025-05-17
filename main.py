#!/usr/bin/env python3
"""
Raspberry Pi Camera Viewer and Frame Capture

This program opens a video stream from a Raspberry Pi camera,
displays it in a window, and allows the user to:
- Capture frames by pressing the spacebar
- Exit the program by pressing 'q'

Captured frames are saved in the 'frames' folder with timestamped filenames.
"""

import cv2
import time
import os
from datetime import datetime
from picamera2 import Picamera2

def main():
    # Create the frames directory if it doesn't exist
    frames_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Initialize the camera
    print("Initializing camera...")
    picam2 = Picamera2()
    
    # Configure the camera
    # You can adjust these settings based on your requirements
    config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)})
    picam2.configure(config)
    
    # Start the camera
    picam2.start()
    print("Camera started successfully")
    
    # Display the video stream and handle keyboard input
    print("Displaying video stream. Press SPACEBAR to capture a frame, 'q' to quit.")
    frame_count = 0
    
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()
        
        # Convert the frame from RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Display live feed
        cv2.imshow("Raspberry Pi Camera", frame_bgr)
        
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
            cv2.imwrite(filepath, frame_bgr)
            frame_count += 1
            print(f"Frame captured: {filename}")
    
    # Clean up
    cv2.destroyAllWindows()
    picam2.stop()
    print(f"Program ended. {frame_count} frames captured.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()
