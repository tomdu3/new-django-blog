from . import views
from django.urls import path

urlpatterns = [
    path('', views.AboutMe.as_view(), name='about'),
]