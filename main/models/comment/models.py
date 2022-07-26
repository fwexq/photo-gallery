from django.db import models
from main.models import Post, CustomUser


class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='id пользователя')
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE, verbose_name='id поста')
    text = models.TextField("")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')



    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at',)




