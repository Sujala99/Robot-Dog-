import face_recognition
import pickle

def load_encoded_faces():
    with open('encoded_faces.pkl', 'rb') as f:
        return pickle.load(f)

def recognize_face(image, encoded_faces):
    unknown_encodings = face_recognition.face_encodings(image)
    if not unknown_encodings:
        return None
    
    unknown_encoding = unknown_encodings[0]
    for name, encodings in encoded_faces.items():
        matches = face_recognition.compare_faces(encodings, unknown_encoding)
        if True in matches:
            return name
    return None
