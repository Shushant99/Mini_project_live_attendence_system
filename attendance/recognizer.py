import face_recognition
import numpy as np
from attendance.models import Student

def load_all_encodings():
    students = Student.objects.exclude(face_encoding=None)
    encodings = []
    ids = []
    for s in students:
        enc = np.frombuffer(s.face_encoding, dtype=np.float64)
        encodings.append(enc)
        ids.append(s.id)
    return ids, encodings


def recognize_face(frame):
    rgb = frame[:, :, ::-1]
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    student_ids, known_encs = load_all_encodings()
    results = []

    for enc, loc in zip(encodings, locations):
        distances = face_recognition.face_distance(known_encs, enc)
        if len(distances) == 0:
            continue

        best = np.argmin(distances)
        if distances[best] < 0.5:
            results.append({
                "student_id": student_ids[best],
                "distance": distances[best],
                "location": loc
            })
    return results
