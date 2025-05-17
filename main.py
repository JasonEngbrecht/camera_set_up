#!/usr/bin/env python3
"""
Raspberry Pi Global Shutter Camera Viewer and Frame Capture

This program opens a video stream from the Raspberry Pi Global Shutter Camera,
displays it in a window, and allows the user to:
- Capture frames by pressing the spacebar
- Exit the program by pressing 'q'

Captured frames are saved in the 'frames' folder with timestamped filenames.
"""

import cv2
import time
import os
import subprocess
from datetime import datetime

def get_camera_details():
    """Get camera details using v4l2-ctl command line tool."""
    try:
        result = subprocess.run(['v4l2-ctl', '--list-formats-ext'], 
                               stdout=subprocess.PIPE, 
                               text=True)
        print("Available camera formats:")
        print(result.stdout)
    except Exception as e:
        print(f"Could not get camera details: {e}")

def main():
    # Create the frames directory if it doesn't exist
    frames_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Print camera details to help with debugging
    get_camera_details()
    
    # Initialize the camera using OpenCV's VideoCapture
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Start with default settings first to make sure we can get frames
    print("Getting initial camera properties...")
    initial_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    initial_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Initial camera resolution: {initial_width}x{initial_height}")
    
    # Try setting the camera properties (but don't assume it will work)
    print("Attempting to set camera to optimal resolution...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1456)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1088)
    
    # Check what resolution we actually got
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera configured at resolution: {actual_width} x {actual_height}")
    
    # Get a test frame to make sure it's working
    print("Testing frame capture...")
    ret, test_frame = cap.read()
    if not ret or test_frame is None:
        print("WARNING: Failed to capture initial test frame!")
        print("Trying with default camera settings...")
        
        # Release the first capture attempt
        cap.release()
        
        # Try again with default settings
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera on second attempt.")
            return
            
        # Check if we can get a frame now
        ret, test_frame = cap.read()
        if not ret or test_frame is None:
            print("Error: Still cannot capture frames. Please check camera connection.")
            return
    
    # Get actual frame dimensions after successful capture
    if test_frame is not None:
        height, width = test_frame.shape[:2]
        print(f"Successfully captured test frame with dimensions: {width}x{height}")
    
    print("Camera initialized successfully")
    print("Displaying video stream. Press SPACEBAR to capture a frame, 'q' to quit.")
    
    frame_count = 0
    
    # Adding a short delay to ensure camera is fully initialized
    time.sleep(1)
    
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        
        if not ret or frame is None:
            print("Warning: Failed to capture frame, retrying...")
            time.sleep(0.1)  # Short delay before retry
            continue  # Skip this iteration and try again
        
        # Get the current frame dimensions
        height, width = frame.shape[:2]
        
        # If the frame is very large, resize it for display purposes only
        display_frame = frame
        max_display_width = 1024
        if width > max_display_width:
            scale_factor = max_display_width / width
            display_frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
        
        # Display live feed (display_frame might be resized for viewing)
        cv2.imshow("Raspberry Pi Camera", display_frame)
        
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
            
            # Save the frame at full resolution
            success = cv2.imwrite(filepath, frame)
            if success:
                frame_count += 1
                print(f"Frame captured: {filename} at {width}x{height}")
            else:
                print(f"Error: Failed to save frame to {filepath}")
    
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
