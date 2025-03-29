import cv2

from notification_utils import send_telegram_alert

# Set up camera motion capture
cam = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

status_list = []
while True:
    # status is a flag that indicates whether the object is currently in the frame
    # 0: object not in frame, 1: object in frame
    status = 0

    ret, frame = cam.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask, (21, 21), 0)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 20000]

    for cnt in filtered_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if rectangle.any():
            status = 1  # object is currently in the frame

    status_list.append(status)
    status_list = status_list[-2:]  # Keep only the last two statuses in the status_list

    if status_list == [1, 0]:
        send_telegram_alert()

    cv2.imshow('Camera Feed', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release camera capture object
cam.release()
cv2.destroyAllWindows()
