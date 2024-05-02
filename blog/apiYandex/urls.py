from django.urls import path
from .views import generate_text

urlpatterns = [
    path('generate_text/', generate_text, name='generate_text'),
]