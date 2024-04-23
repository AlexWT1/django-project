from django.urls import path
from . import views
from .models import LikedPostsView

urlpatterns = [
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='post_create'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('liked_posts/', LikedPostsView.as_view(), name='liked_posts'),
]
