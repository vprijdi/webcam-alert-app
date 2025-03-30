import shutil
import cv2
import datetime
import os
import atexit
from notification_utils import send_telegram_alert


TEMP_DIR = "images"


def remove_folder():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


atexit.register(remove_folder)

# Set up camera motion capture
cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

# Create directory to temporarily store frames where motion is detected by the camera
os.makedirs(TEMP_DIR, exist_ok=True)

status_list = []
frame_count = 0
while True:
    # status is a flag that indicates whether the object is currently in the frame
    # 0: object not in frame, 1: object in frame
    status = 0

    ret, frame = cam.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Calculate bottom-right position
    text_size = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = width - text_size[0] - 10
    text_y = height - 10

    # Add timestamp to frame
    cv2.putText(img=frame, text=timestamp, org=(text_x, text_y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=(0, 255, 255), thickness=2, lineType=cv2.LINE_AA)

    # Apply background subtraction to detect foreground objects in the current frame
    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    # Find contours in the foreground mask
    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 20000]

    # Draw bounding rectangles around the detected objects
    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if rectangle.any():
            status = 1  # object is currently in the frame
            cv2.imwrite(f"{TEMP_DIR}\\image{frame_count}.png", frame)
            frame_count += 1

    status_list.append(status)
    status_list = status_list[-2:]  # Keep only the last two statuses in the status_list

    # Send alert when object leaves frame (when status changes from 1 to 0)
    if status_list == [1, 0]:
        image = f"{TEMP_DIR}\\image{int(frame_count / 2)}.png"
        send_telegram_alert(image)

    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera capture object
cam.release()
cv2.destroyAllWindows()
