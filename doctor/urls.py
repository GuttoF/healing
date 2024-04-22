from django.urls import path
from . import views

urlpatterns = [
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
]
