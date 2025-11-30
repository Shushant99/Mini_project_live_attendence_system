import os
import django
import face_recognition
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_attendance.settings")
django.setup()

from attendance.models import Student

for s in Student.objects.all():
    img = face_recognition.load_image_file(s.photo.path)
    encs = face_recognition.face_encodings(img)
    if encs:
        s.face_encoding = encs[0].tobytes()
        s.save()
        print("Encoding saved for", s.name)
