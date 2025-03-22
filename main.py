import cv2


# Set up camera capture
cam = cv2.VideoCapture(0)
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

while True:
    ret, frame = cam.read()
    out.write(frame)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break
