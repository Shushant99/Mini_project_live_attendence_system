from django.db import models
from django.contrib.auth.models import User
import uuid
import numpy as np

class Profile(models.Model):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
        ("head", "Head Admin"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="students/")
    face_encoding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class ClassSession(models.Model):
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} @ {self.date}"


class AttendanceRecord(models.Model):
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    confidence = models.FloatField(default=0.0)
    capture = models.ImageField(upload_to="captures/", null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} at {self.timestamp}"
