from . import views
from django.urls import path

urlpatterns = [
    path("", views.Postlist.as_view(), name="home"),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]