from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from attendance import views as attendance_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("attendance/", include("attendance.urls")),
    path('accounts/', include('django.contrib.auth.urls')), 
    path("", RedirectView.as_view(url="/attendance/", permanent=False)),
    
]