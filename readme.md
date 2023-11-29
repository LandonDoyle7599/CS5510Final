# Project Summary

### How to run

To run the project, first create a virtual environment and install the requirements using the following commands:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then, run the following command to run the project:

```python3 MoveToBall.py```

To change the color of the ball the robot will seek, change the ball_color variable on line 17 of MoveToBall.py. The current options are red, blue, green, and yellow.

## Project Description
MoveToBall.py is the solution file representing our finished project. This code starts by rotating the robot until the camera detects a sphere of the specified color (using opencv). It then begins taking discrete frames and determines if the ball is to the left or right of the robot. If the ball is to the left, the robot turns left. If the ball is to the right, the robot turns right. If the ball is in the center, the robot moves forward. The robot will continue to move forward until the ball is within a certain threshold distance of the sonar. Once it reaches that point the ball will move forward to ensure attachment, and then begin reversing all the navigational commands it has processed thus far in reverse order and with reverse magnitude to return the ball to the goal, which is the starting point of the robot. 

Below are links to two videos showing the robot seeking 2 balls of different colors. [Video 1](https://photos.app.goo.gl/qtus6Wq3s6q7FtP16) represents the ability of the program to operate when the ball as at a distance from the robot. [Video 2](https://photos.app.goo.gl/i1nyLGzqBo46stxs5) represents the ability of the robot to rotate until it discovers the ball if it does not start oriented in that direction.

## Incremental Files

The file Car.py contains provided class code to control the raspbot

SonarTest.py is a file to test the sonar sensor, this was also provided in class.

The file DetectBall implements colored ball detection using any camera without moving the robot. This was our first deliverable as we wanted to ensure we could reliably detect a ball of a specified color before working on navigating the robot.

Reckoning.py is another incremental file for dead reckoning control of the robot to practice basic mobility commands. This was created for the first homework assignment.

StopCar.py is a file that stops the car in case it gets stuck on a command.

TestDistance.py is another incremental file to determine the distance an object is from the robot, this was created to work towards the robot knowing when it had reached the ball. After determining we could not reliably detect if we had reached the robot using the camera, we switched to using sonar and used this file to determine the threshold we needed to use for when the robot is close enough to the ball.

TestReverseCommands.py was another incremental file to test backtracking along a path with the robot. After we decided to bring the ball to the goal using reversed commands, this decision was based on the relatively low performance of the raspberry pi 3, we created this file to test how to reverse commands and scale the power to factor in the weight of the ball.