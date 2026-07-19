from django.urls import path
from . import views

app_name = "beauty"

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book_appointment, name="book_appointment"),
]
