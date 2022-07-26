import os
import urllib.request

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models
from main.models.user.manager import UserManager


class CustomUser(AbstractUser):
    username = None
    last_login = None
    date_joined = None

    first_name = models.CharField(max_length=40, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=40, unique=True, verbose_name='email aдрес')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия пользователя')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    avatar = models.ImageField(upload_to='user/images', max_length=1024, default='user/images/default_avatar.jpg', verbose_name="Аватар")
    api_key = models.CharField(max_length=60, verbose_name='API ключ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email


    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
