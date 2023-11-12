from Car import Car
import time

prevCommands = []
car = Car()
car.control_car(75, 75)
time.sleep(2)
prevCommands.append((-75, -75))
car.stop()
car.control_car(-75, 75)
time.sleep(2)
prevCommands.append((75, -75))
car.stop()
car.control_car(75,-75)
time.sleep(2)
prevCommands.append((-75, 75))
car.stop()

for command in prevCommands:
    car.stop()
    print(command)
    car.control_car(command[0], command[1])
    time.sleep(2)