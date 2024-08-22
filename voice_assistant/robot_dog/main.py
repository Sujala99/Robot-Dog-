from robot_dog.controller import DogRobotController
import time

if __name__ == "__main__":
    controller = DogRobotController()
    controller.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
