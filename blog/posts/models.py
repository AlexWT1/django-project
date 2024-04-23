from django.db import models
from django.http import JsonResponse
from django.views import View
from users.models import User


class LikedPostsView(View):
    def get(self, request, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user
        # Получаем список постов, лайкнутых пользователем
        liked_posts = Post.objects.filter(likes=user)
        # Создаем список ID лайкнутых постов
        liked_posts_ids = [post.id for post in liked_posts]
        # Возвращаем список ID в формате JSON
        return JsonResponse({'likedPosts': liked_posts_ids})


class PostManager(models.Manager):
    def get_posts_by_likes(self, min_likes=0):
        return self.get_queryset().filter(likes__count__gte=min_likes)


# Create your models here.
class Post(models.Model):
    objects = PostManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_liked_by_user(self, user):
        return self.likes.filter(id=user.id).exists()


class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
