import cv2
import numpy as np

def detect_ball(frame, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if color == "red":
        lower_bound = np.array([0, 100, 100])
        upper_bound = np.array([10, 255, 255])
    elif color == "yellow":
        lower_bound = np.array([20, 100, 100])
        upper_bound = np.array([40, 255, 255])
    elif color == "blue":
        lower_bound = np.array([90, 100, 100])
        upper_bound = np.array([130, 255, 255])
    elif color == "green":
        lower_bound = np.array([40, 100, 100])
        upper_bound = np.array([80, 255, 255])
    elif color == "grey":
        lower_bound = np.array([0, 0, 100])
        upper_bound = np.array([255, 20, 200])

    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            width, _ = frame.shape[:2]
            if cx < width // 3:
                position = "Left"
            elif cx > 2 * width // 3:
                position = "Right"
            else:
                position = "Center"
            return position

    return "Not Detected"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    color = "green"  # Change to the desired color

    ball_position = detect_ball(frame, color)

    cv2.putText(frame, f"Ball: {ball_position}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Ball Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
