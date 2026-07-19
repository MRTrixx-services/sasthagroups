from django.urls import path
from . import views

app_name = "flowers"

urlpatterns = [
    path("", views.home, name="home"),
    path("enquiry/", views.flower_enquiry, name="flower_enquiry"),
]
