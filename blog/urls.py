from . import views
from django.urls import path

urlpatterns = [
    path("", views.Postlist.as_view(), name="home"),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit_comment/<int:comment_id>', views.CommentEditView.as_view(), name='comment_edit'),
]