from django.urls import path
from .views import home,mobiles,contact_view

urlpatterns = [
    path('', home, name='home'),
    path("mobiles/", mobiles, name="mobiles"),
    path('contact/', contact_view, name='contact'),
]