import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
from Car import Car

# Define the colors for ball detection (you can adjust these values)
yellow_lower = np.array([20, 75, 75])
yellow_upper = np.array([40, 255, 255])
green_lower = np.array([40, 75, 75])
green_lower = np.array([40, 100, 100])
green_upper = np.array([80, 255, 255])
blue_lower = np.array([90, 75, 75])
blue_upper = np.array([130, 255, 255])

# Initialize your car class (modify this to match your actual class)


# Initialize the webcam
cap = cv2.VideoCapture(0)
car = Car()

GPIO.setwarnings(False)

EchoPin = 18
TrigPin = 16

GPIO.setmode(GPIO.BOARD)

GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)

def distance():
    GPIO.output(TrigPin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03:
            return -1
    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if (t5 - t1) > 0.03:
            return -1

    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1) * 340 / 2) * 100

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
        continue

    if is_ball_in_frame(frame, ball_color):
        break

    car.control_car(-75, 75)
    time.sleep(.5)
    car.control_car(0,0)
    time.sleep(.01)
print("Found Ball")    

prevLeft = []
prevRight = []

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the mask for the selected color (yellow or green)
    if ball_color == "yellow":
        mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    elif ball_color == "green":
        mask = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
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
            if cx < frame_center - 40:
                car.control_car(-75,75)
                prevLeft.append(75)
                prevRight.append(-75)
                time.sleep(.1)
                car.control_car(0,0)
                time.sleep(.01)
                if abs(distance()) <= .5:
                    print("Got to Ball")
                    break
            elif cx > frame_center + 40:
                car.control_car(75,-75)
                prevLeft.append(-75)
                prevRight.append(75)
                time.sleep(.1)
                car.control_car(0,0)
                time.sleep(.01)
                if abs(distance()) <= .5:
                    print("Got to Ball")
                    break
            else:
                car.control_car(75,75)
                prevLeft.append(-75)
                prevRight.append(-75)
                time.sleep(.1)
                car.control_car(0,0)
                time.sleep(.01)
                if abs(distance()) <= .5:
                    print("Got to Ball")
                    break
    else:
        car.control_car(-75,75)
        time.sleep(.1)
        car.control_car(0,0)
        time.sleep(.01)

    # Display the frame

    # Break the loop if a key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        car.control_car(0,0)
        time.sleep(.01)
        break

prevLeft.reverse()
prevRight.reverse()
for x in range(len(prevLeft)):
    car.control_car(prevLeft[x]*2, prevRight[x]*2)
    time.sleep(.1)
    car.control_car(0,0)
    time.sleep(.05)


# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
