from Car import Car
import time

if __name__ == '__main__':
    car = Car()
    prevLeft = []
    prevRight = []
    left = 50
    right = 50
    for x in range(4):
        car.control_car(left, right)
        prevLeft.append(-50)
        prevRight.append(-50)
        time.sleep(2)
        car.control_car(0, 0)
        time.sleep(.1)
        car.control_car(3*left, -3*right)
        prevLeft.append(-150)
        prevRight.append(150)
        time.sleep(.8)
        car.control_car(0, 0)
        time.sleep(.1)
    car.control_car(0, 0)

    prevLeft.reverse()
    prevRight.reverse()
    index = 0
    for val in prevLeft:
        car.control_car(val, prevRight[0])
        time.sleep(2)
        car.control_car(0, 0)
        time.sleep(.1)
        car.control_car(prevLeft[x], prevRight[x])
        time.sleep(.8)
        car.control_car(0, 0)
        time.sleep(.1)