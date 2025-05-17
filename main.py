#!/usr/bin/env python3
"""
Raspberry Pi Global Shutter Camera Viewer and Frame Capture

This program opens a video stream from the Raspberry Pi Global Shutter Camera at full resolution,
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
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Set camera properties to full resolution for the Raspberry Pi Global Shutter Camera
    # The Sony IMX296 sensor has a native resolution of 1456 × 1088
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1456)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1088)
    
    # You might need to set other camera properties for optimal performance
    # Uncomment if needed
    # cap.set(cv2.CAP_PROP_FPS, 30)  # Set target FPS
    # cap.set(cv2.CAP_PROP_EXPOSURE, -1)  # Auto exposure
    
    # Check what resolution we actually got (might not match request exactly)
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"Camera started successfully at resolution: {int(actual_width)} x {int(actual_height)}, {actual_fps} FPS")
    print("Displaying video stream. Press SPACEBAR to capture a frame, 'q' to quit.")
    
    frame_count = 0
    
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Get the current frame dimensions
        height, width = frame.shape[:2]
        
        # If the frame is very large, resize it for display purposes only
        # (the saved image will still be full resolution)
        display_frame = frame
        if width > 1024:
            scale_factor = 1024 / width
            display_frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
        
        # Display live feed (display_frame might be resized for viewing)
        cv2.imshow("Raspberry Pi Global Shutter Camera", display_frame)
        
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
            
            # Save the frame at FULL RESOLUTION
            cv2.imwrite(filepath, frame)
            frame_count += 1
            print(f"Frame captured: {filename} at {width}x{height}")
    
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
