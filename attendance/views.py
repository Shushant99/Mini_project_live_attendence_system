from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.utils import timezone
import base64
import cv2
import numpy as np
from attendance.models import AttendanceRecord, ClassSession, Student
from attendance.recognizer import recognize_face
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Profile, Student
from django.contrib.auth.models import User
@api_view(["POST"])
def live_frame(request):
    frame_data = request.data.get("frame")

    raw = base64.b64decode(frame_data.split(",")[1])
    jpg = np.frombuffer(raw, dtype=np.uint8)
    frame = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    matches = recognize_face(frame)

    for m in matches:
        student = Student.objects.get(id=m["student_id"])
        AttendanceRecord.objects.create(
            session=ClassSession.objects.last(),
            student=student,
            confidence=float(1 - m["distance"]),
        )

    return Response({"detected": len(matches)})
def register(request):
    """
    Simple register view. On register, create Profile with role selected.
    In production: add email verification, stronger validation.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        role = request.POST.get("role", "student")
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, role=role)
            # if student, create Student record (optional)
            if role == "student":
                Student.objects.create(profile=user.profile, roll_number=f"R{user.id}", name=user.username)
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "attendance/register.html", {"form": form})


def custom_login(request):
    """
    Login with 'remember me' checkbox. If remember checked, set session expiry longer.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        remember = request.POST.get("remember", None)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if remember:
                # Keep session for SESSION_COOKIE_AGE (set in settings)
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                # Expires on browser close
                request.session.set_expiry(0)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "attendance/login.html", {"form": form})


@login_required
def dashboard(request):
    # example: show session summary; tailor by role
    profile = request.user.profile
    context = {"profile": profile}
    return render(request, "attendance/dashboard.html", context)