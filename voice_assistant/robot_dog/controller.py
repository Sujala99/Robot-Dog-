import cv2
import time
import numpy as np
import onnxruntime
from xgolib import XGO
import threading
import random
import atexit

# Import face recognition functions
from face_recognition.recognize import load_encoded_faces, recognize_face
from .detection import detect_objects
from .utils import distance_finder

# Constants defining camera resolution and known parameters for distance calculation
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
KNOWN_DISTANCE = 76.2  # Example known distance from the camera to a face
KNOWN_WIDTH = 14.3     # Example known width of the face
FOCAL_LENGTH = 500     # Preset focal length of the camera

class DogRobotController:
    def __init__(self):
        self.dog = XGO('COM4', 115200, 'xgolite')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, CAMERA_WIDTH)
        self.cap.set(4, CAMERA_HEIGHT)
        self.session = onnxruntime.InferenceSession('/home/pi/model/Model.onnx')
        self.encoded_faces = load_encoded_faces()
        self.stop_thread = False
        self.t = None

    def move_robot_based_on_distance(self, distance, target_distance=50, too_close_distance=10):
        if distance > target_distance:
            self.dog.move('x', 10)
        elif distance < too_close_distance:
            self.dog.stop()
            time.sleep(1)
            self.dog.move('y', -5 if random.choice([True, False]) else 5)
            time.sleep(1)
            self.dog.stop()
        else:
            self.dog.stop()

    def move_robot_based_on_position(self, object_center_x, frame_width):
        center_tolerance = frame_width * 0.2
        center_range = (frame_width / 2 - center_tolerance, frame_width / 2 + center_tolerance)

        if object_center_x < center_range[0]:
            self.dog.move('y', -5)
        elif object_center_x > center_range[1]:
            self.dog.move('y', 5)
        else:
            self.dog.move('x', 10)

    def run(self):
        KNOWN_WIDTH = 14.3
        focal_length_found = 500
        frame_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        target_distance = 50

        while not self.stop_thread:
            _, frame = self.cap.read()

            bboxes = detect_objects(self.session, frame)
            if bboxes:
                for bbox in bboxes:
                    if int(bbox[5]) == 0:
                        x1, y1, x2, y2 = bbox[:4]
                        object_width_in_frame = x2 - x1
                        object_center_x = (x1 + x2) / 2
                        distance = distance_finder(focal_length_found, KNOWN_WIDTH, object_width_in_frame)
                        print(f"Distance to object: {distance} cm")

                        face_image = frame[y1:y2, x1:x2]
                        name = recognize_face(face_image, self.encoded_faces)
                        if name:
                            print(f"Hello, {name}!")
                            # Optionally, have the robot speak the name
                            self.speak(f"Hello, {name}!")
                        
                        self.move_robot_based_on_position(object_center_x, frame_width)
                        self.move_robot_based_on_distance(distance, target_distance)
                        break
            else:
                print("No person detected. Turning to search...")
                self.dog.move('y', 5)
                time.sleep(1)
                self.dog.stop()

    def start(self):
        self.t = threading.Thread(target=self.run)
        self.t.start()

    def stop(self):
        self.stop_thread = True
        if self.t:
            self.t.join()
        cv2.destroyAllWindows()
