from django.urls import path
from . import views
from .models import LikedPostsView
from .views import DeleteCommentView

urlpatterns = [
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='post_create'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('liked_posts/', LikedPostsView.as_view(), name='liked_posts'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('my_posts/', views.MyPostsView.as_view(), name='my_posts'),
    path('liked-posts/', views.liked_posts, name='liked_posts'),
]
