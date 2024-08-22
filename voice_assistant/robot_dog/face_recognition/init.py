import os
import face_recognition
import pickle

def capture_and_encode_faces(data_path):
    encoded_faces = {}
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                img_path = os.path.join(root, file)
                label = os.path.basename(root)
                image = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(image)[0]
                if label in encoded_faces:
                    encoded_faces[label].append(encoding)
                else:
                    encoded_faces[label] = [encoding]
    
    with open('encoded_faces.pkl', 'wb') as f:
        pickle.dump(encoded_faces, f)

# Call this function with the path to your dataset
capture_and_encode_faces('data/faces')
