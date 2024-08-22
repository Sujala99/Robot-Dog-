
import cv2
import numpy as np
import pyttsx3
import time
from cvlib.object_detection import draw_bbox

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use the configured voice ID
engine.setProperty('rate', 180)    # Speed in words per minute
engine.setProperty('volume', 1.0)  # Volume level (0.0 to 1.0)
engine.setProperty('pitch', 1.1)   # Pitch of the voice (0.5 to 2.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def detect_faces(config_path, weights_path, labels_path):
    # Load YOLO
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


    # Load class labels
    with open(labels_path, 'r') as f:
        classes = f.read().strip().split('\n')

    # Get output layer names
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 for default camera

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    start_time = time.time()  # Start time for the camera capture
    detected_labels = []

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Convert frame to blob
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # Perform forward pass inference
        outputs = net.forward(output_layers)

        # Initialize lists for bounding boxes, confidences, and class IDs
        bbox = []
        confidences = []
        class_ids = []

        # Process each output layer
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Filter out weak predictions by ensuring confidence threshold is met
                if confidence > 0.5:
                    # Scale bounding box coordinates to the original frame
                    box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    (centerX, centerY, width, height) = box.astype("int")

                    # Calculate coordinates for the top-left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    bbox.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(bbox, confidences, 0.5, 0.4)

        # Ensure at least one detection exists
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = bbox[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = [int(c) for c in np.random.randint(0, 255, size=(3,))]

                # Draw bounding box and label on the image
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = f"{label}: {confidence:.2f}"
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Add detected label to the list
                detected_labels.append(label)

        # Display the resulting frame
        cv2.imshow('Object Detection', frame)
        
        # Break the loop after 8 seconds
        if time.time() - start_time >= 8:
            break

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

    # Announce detected labels
    if detected_labels:
        unique_labels = list(set(detected_labels))  # Remove duplicates
        speak("I see " + ", ".join(unique_labels))
        
    else:
        speak("I didn't see anything.")

# Example usage
# Paths to the YOLO config, weights, and class names files
config_path = './yolo/yolov4.cfg'
weights_path = './yolo/yolov4.weights'
labels_path = './yolo/coco.names'


