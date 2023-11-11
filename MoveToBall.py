import cv2
import numpy as np
import time
from Car import Car

# Define the colors for ball detection (you can adjust these values)
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([40, 255, 255])
green_lower = np.array([40, 40, 40])
green_upper = np.array([80, 255, 255])

# Initialize your car class (modify this to match your actual class)


# Initialize the webcam
cap = cv2.VideoCapture(0)
car = Car()

def is_ball_in_frame(frame, color):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the mask for the selected color (yellow or green)
    if color == "yellow":
        mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    elif color == "green":
        mask = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return bool(contours)

# Initialize the car object

# Rotate the car left until a ball is detected
ball_color = "yellow"  # Change this to "yellow" if needed
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    if is_ball_in_frame(frame, ball_color):
        break

    car.control_car(-75, 75)
    time.sleep(1)
    car.stop()

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    if is_ball_in_frame(frame, ball_color):
        # Find the largest contour (the ball)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M['m00'] != 0:
            # Calculate the centroid of the ball
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Get the frame center
            frame_center = frame.shape[1] // 2

            # Determine if the ball is left, right, or center
            if cx < frame_center - 20:
                car.control_car(-75,75)
                time.sleep(1)
                car.stop()
            elif cx > frame_center + 20:
                car.control_car(75,-75)
                time.sleep(1)
                car.stop()
            else:
                car.control_car(75,75)
                time.sleep(1)
                car.stop()

    # Display the frame
    # Break the loop if a key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        car.stop()
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
