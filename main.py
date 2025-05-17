#!/usr/bin/env python3
"""
Raspberry Pi Global Shutter Camera Viewer and Frame Capture using Picamera2

This program opens a video stream from the Raspberry Pi Global Shutter Camera,
displays it in a window, and allows the user to:
- Capture frames by pressing the spacebar
- Exit the program by pressing 'q'

Captured frames are saved in the 'frames' folder with timestamped filenames.
"""

import sys
import os
import time
import subprocess
import cv2
import numpy as np
from datetime import datetime

def check_dependencies():
    """Check if the required dependencies are installed."""
    print("\n----- CHECKING DEPENDENCIES -----")
    
    # Check if picamera2 is installed in system packages
    try:
        result = subprocess.run(["apt", "list", "--installed", "python3-picamera2"], 
                               capture_output=True, text=True, check=False)
        if "python3-picamera2" in result.stdout and "installed" in result.stdout:
            print("✓ python3-picamera2 is installed via apt")
        else:
            print("✗ python3-picamera2 is NOT installed via system packages")
            print("  Try: sudo apt install python3-picamera2")
    except Exception as e:
        print(f"? Error checking apt packages: {e}")
    
    # Check for libcamera
    try:
        result = subprocess.run(["apt", "list", "--installed", "libcamera*"], 
                               capture_output=True, text=True, check=False)
        if "libcamera" in result.stdout and "installed" in result.stdout:
            print("✓ libcamera packages are installed")
        else:
            print("✗ libcamera packages might be missing")
            print("  Try: sudo apt install libcamera-apps")
    except Exception as e:
        print(f"? Error checking libcamera: {e}")
    
    # Check camera tools
    try:
        result = subprocess.run(["which", "libcamera-hello"], 
                               capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("✓ libcamera tools are installed")
        else:
            print("✗ libcamera-hello command not found")
            print("  Try: sudo apt install libcamera-apps")
    except Exception as e:
        print(f"? Error checking camera tools: {e}")
    
    print("---------------------------------")
    print("\n----- TROUBLESHOOTING SUGGESTIONS -----")
    print("1. Install picamera2 with system packages (preferred method):")
    print("   sudo apt update")
    print("   sudo apt install -y python3-picamera2 libcamera-apps")
    print("\n2. Make sure the camera is enabled:")
    print("   sudo raspi-config")
    print("   (Navigate to Interface Options > Camera > Enable)")
    print("\n3. Check if camera is detected:")
    print("   vcgencmd get_camera")
    print("   (Should show 'supported=1 detected=1')")
    print("\n4. Test camera with system tools:")
    print("   libcamera-hello --list-cameras")
    print("   libcamera-jpeg -o test.jpg")
    print("\n5. Ensure your user is in the 'video' group:")
    print("   sudo usermod -aG video $USER")
    print("   (Log out and back in for this to take effect)")
    print("-----------------------------------------")

def main():
    # Check dependencies
    check_dependencies()
    
    # Create the frames directory if it doesn't exist
    frames_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    # Import picamera2 here to handle import errors more gracefully
    try:
        from picamera2 import Picamera2
        print("\n✓ Successfully imported picamera2")
    except ImportError as e:
        print(f"\n✗ Failed to import picamera2: {e}")
        print("\nTo install picamera2 correctly, follow these steps:")
        print("1. Exit any virtual environments")
        print("2. Run: sudo apt install python3-picamera2")
        print("3. Use the system Python instead of a virtual environment")
        print("   or install picamera2 in your virtual environment with:")
        print("   pip install picamera2")
        return
    except Exception as e:
        print(f"\n✗ Unexpected error importing picamera2: {e}")
        return
    
    # Initialize camera
    print("\nInitializing Picamera2...")
    try:
        picam2 = Picamera2()
        
        # List available cameras
        cameras = picam2.global_camera_info()
        if cameras:
            print(f"Available cameras: {len(cameras)}")
            for i, camera in enumerate(cameras):
                print(f"Camera {i}: {camera.get('Model', 'Unknown')} ({camera.get('Location', 'Unknown location')})")
        else:
            print("No cameras detected by Picamera2")
            return
        
        # Set up camera configuration
        print("Setting up camera configuration...")
        
        # For Global Shutter Camera, use full resolution (1456x1088)
        # but fall back to default if that fails
        try:
            # Try to set the full resolution for the Global Shutter Camera
            config = picam2.create_preview_configuration(
                main={"size": (1456, 1088), "format": "RGB888"}
            )
            picam2.configure(config)
            print("Using full resolution: 1456x1088")
        except Exception as e:
            print(f"Error setting full resolution: {e}")
            print("Falling back to default configuration...")
            config = picam2.create_preview_configuration()
            picam2.configure(config)
        
        # Start the camera
        print("Starting camera...")
        picam2.start()
        
        # Get camera info after starting
        sensor_resolution = picam2.camera_properties.get('PixelArraySize', (0, 0))
        print(f"Sensor resolution: {sensor_resolution[0]}x{sensor_resolution[1]}")
        
        # Get frame dimensions
        test_frame = picam2.capture_array()
        if test_frame is not None:
            print(f"Captured frame size: {test_frame.shape[1]}x{test_frame.shape[0]}x{test_frame.shape[2]}")
        else:
            print("Failed to capture initial test frame")
            picam2.close()
            return
        
        print("\nCamera started successfully!")
        print("- Press SPACEBAR to capture a frame")
        print("- Press 'q' to quit")
        
        frame_count = 0
        
        while True:
            # Capture frame
            frame = picam2.capture_array()
            
            # Convert from RGB to BGR for OpenCV display
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Display frame
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
                
                # Save the frame (convert from RGB to BGR for OpenCV imwrite)
                success = cv2.imwrite(filepath, frame_bgr)
                if success:
                    frame_count += 1
                    print(f"Frame captured: {filename}")
                else:
                    print(f"Error: Failed to save frame to {filepath}")
        
        # Clean up
        picam2.close()
        cv2.destroyAllWindows()
        print(f"Program ended. {frame_count} frames captured.")
    
    except Exception as e:
        print(f"Camera error: {e}")
        print("\nAdditional troubleshooting:")
        print("1. Make sure you're not running in a virtual environment")
        print("2. Ensure the camera cable is properly connected")
        print("3. Check if the camera is enabled in raspi-config")
        print("4. Try rebooting your Raspberry Pi")
        print("5. Run 'libcamera-hello' to test if the camera works with libcamera")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()
