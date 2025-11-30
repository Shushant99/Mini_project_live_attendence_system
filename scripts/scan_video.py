import cv2
import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_attendance.settings")
django.setup()

from attendance.recognizer import recognize_face
from attendance.models import AttendanceRecord, ClassSession, Student

cap = cv2.VideoCapture("video.mp4")
session = ClassSession.objects.last()

while True:
    ret, frame = cap.read()
    if not ret: break

    matches = recognize_face(frame)
    for m in matches:
        student = Student.objects.get(id=m["student_id"])
        AttendanceRecord.objects.create(
            session=session,
            student=student,
            confidence=float(1 - m["distance"]),
        )
