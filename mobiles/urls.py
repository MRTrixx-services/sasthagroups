from django.urls import path
from .views import home,mobiles

urlpatterns = [
    path('', home, name='home'),
    path("mobiles/", mobiles, name="mobiles"),

]