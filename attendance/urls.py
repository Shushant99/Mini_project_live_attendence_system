from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
app_name = "attendance"
urlpatterns = [
    path("live-frame/", views.live_frame, name="live_frame"),
    path("login/", views.custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register, name="register"),
    path("", views.dashboard, name="dashboard"),  # teacher dashboard/home.
    # path("live/", views.live_view, name="live")
     path("admin/", admin.site.urls),
   
]
