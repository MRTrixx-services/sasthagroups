from django.urls import path
from . import views

app_name = "flowers"

urlpatterns = [
    path("", views.home, name="home"),
]