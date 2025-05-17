# Raspberry Pi Camera Viewer and Frame Capture

A simple application to view the Raspberry Pi camera feed and capture individual frames.

## Features

- Live video stream from Raspberry Pi camera
- Capture individual frames with spacebar
- Save frames with timestamped filenames
- Exit program with 'q' key

## Setup

1. Ensure your Raspberry Pi camera is properly connected and enabled.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the program:
   ```
   python main.py
   ```

## Usage

- Press **SPACEBAR** to capture and save the current frame
- Press **q** to quit the application

## Saved Frames

Captured frames are saved in the `frames` directory with timestamped filenames in the format:
```
frame_YYYYMMDD_HHMMSS_N.jpg
```

## Troubleshooting

- If you encounter a "Camera not found" error, ensure the camera is properly connected and enabled in Raspberry Pi configuration.
  
- To enable the camera using `raspi-config`:
  ```
  sudo raspi-config
  ```
  Navigate to "Interface Options" > "Camera" > "Yes" to enable the camera.

- After enabling the camera, reboot your Raspberry Pi:
  ```
  sudo reboot
  ```

## Notes for Global Shutter Camera

The Raspberry Pi Global Shutter Camera may require specific configuration for optimal performance. The current settings are configured with reasonable defaults, but you may need to adjust parameters like exposure, gain, or white balance depending on your specific use case.
