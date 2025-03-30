# Webcam Motion Detector

A simple Python application that detects motion using your webcam and sends alerts via Telegram when objects enter and leave the frame.

## Overview

This project uses OpenCV to access your webcam feed and detect motion by applying background subtraction. When an object enters the frame and then leaves, the system captures an image and sends it as an alert to a specified Telegram chat.

## Features

- Live webcam monitoring
- Motion detection using background subtraction
- Object tracking with visual bounding boxes
- Timestamp overlay on video feed
- Automatic Telegram notifications when motion is detected
- Automatic cleanup of stored images when the program exits

## Requirements

- Python 3.6+
- OpenCV (`cv2`)
- Requests

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/webcam-motion-detector.git
   cd webcam-motion-detector
   ```

2. Install the required dependencies:
   ```
   pip install opencv-python requests
   ```

3. Set up a Telegram bot:
   - Create a new bot using [BotFather](https://t.me/botfather) and note the token
   - Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)

4. Set up your Telegram credentials:
   
   You have two options:

   **Option 1:** Set environment variables (recommended for security):
   
   In Command Prompt (Windows):
   ```
   setx WEBCAM_ALERT_BOT_TOKEN "your_telegram_bot_token"
   setx WEBCAM_ALERT_BOT_CHATID "your_telegram_chat_id"
   ```
   Note: After using setx, you'll need to open a new Command Prompt window for the changes to take effect.
   If you're running the script from an IDE like PyCharm or VS Code, restart the IDE after setting the variables.

   In Terminal (macOS/Linux):
   ```
   export WEBCAM_ALERT_BOT_TOKEN="your_telegram_bot_token"
   export WEBCAM_ALERT_BOT_CHATID="your_telegram_chat_id"
   ```
   For permanent storage on macOS/Linux, add these exports to your `~/.bashrc` or `~/.zshrc` file.

   **Option 2:** Modify the code directly in `notification_utils.py`:
   
   Change these lines:
   ```python
   token = os.getenv("WEBCAM_ALERT_BOT_TOKEN")
   chat_id = os.getenv("WEBCAM_ALERT_BOT_CHATID")
   ```
   
   To:
   ```python
   token = "your_telegram_bot_token"  # Replace with your actual bot token
   chat_id = "your_telegram_chat_id"  # Replace with your actual chat ID
   ```


## Usage

Run the main script:
```
python main.py
```

- The webcam feed will open in a new window
- Motion will be highlighted with green bounding boxes
- Press 'q' to quit the application
- Images of detected motion will be saved to the `images` folder (automatically cleaned up when the program exits)
- When an object leaves the frame after being detected, an alert will be sent to your Telegram chat

## How It Works

1. The program captures video from your webcam
2. It applies background subtraction to detect moving objects
3. Objects above a certain size threshold (20,000 pixels area) are highlighted
4. When a detected object leaves the frame, a notification is sent via Telegram
5. All captured images are automatically deleted when the program exits

## Files

- `main.py`: The main script that handles webcam capture and motion detection
- `notification_utils.py`: Helper module for sending Telegram notifications

## Customization

You can adjust the motion detection sensitivity by modifying these parameters in `main.py`:

- Change the contour area threshold (currently 20000) to detect smaller or larger objects
- Modify the Gaussian blur parameters for different noise reduction
- Adjust the dilation iterations to change how motion blobs are connected
