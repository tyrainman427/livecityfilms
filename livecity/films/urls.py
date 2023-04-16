from django.urls import path
from .views import *

app_name = 'films'

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('services/', services, name="services"),
    path('pricing/', pricing, name="pricing"),
    path('contact/', contact, name="contact"),
    path('now_playing/', now_playing, name="now_playing"),
]
