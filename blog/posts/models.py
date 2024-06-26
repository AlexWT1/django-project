from django.db import models
from users.models import User


class PostManager(models.Manager):
    def get_posts_by_likes(self, min_likes=0):
        """
        Возвращает все посты с количеством лайков больше или равным указанному значению.

        :param min_likes: Минимальное количество лайков для поста.
        :return: QuerySet объектов Post.
        """
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


class Comment(models.Model):
    objects = models.Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
