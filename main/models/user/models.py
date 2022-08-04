from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from main.models.user.manager import UserManager


class CustomUser(AbstractUser):
    username = None
    last_login = None
    date_joined = None

    first_name = models.CharField(max_length=255, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=255, unique=True, verbose_name='email aдрес')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия пользователя')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    avatar = models.ImageField(upload_to='user/images', max_length=1024, default='user/images/default_avatar.jpg', verbose_name="Аватар")
    api_key = models.CharField(max_length=255, verbose_name='API ключ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    ip = models.CharField(max_length=255, verbose_name='Айпи адрес')
    total_visits = models.IntegerField(default=0, verbose_name='Количество посещений сайта за все время')
    day = models.DateField(default=timezone.now, verbose_name='Сегодняшнее число')
    day_visits = models.IntegerField(default=0, verbose_name='Количество посещений в течение дня')
    count = models.IntegerField(verbose_name='Количество посещений сайта', default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_absolute_url_user(self):
        return reverse('profile', kwargs={'pk': self.pk})