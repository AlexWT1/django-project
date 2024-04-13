from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = 'custom_user'
        managed = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        default_related_name = 'blog_users'

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='blog_users')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True,
                                              related_name='blog_users')