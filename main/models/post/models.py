from django.db import models
from django.urls import reverse
from django.utils import timezone
from main.models import CustomUser
from django.db.models.deletion import get_candidate_relations_to_delete


class Manager(models.Manager):
    def get_queryset(self):
        return super(Manager, self).get_queryset().filter(is_deleted=False)

class IsDeletedMixin(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name='На удаление')

    objects = Manager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        delete_candidates = get_candidate_relations_to_delete(self.__class__._meta)
        if delete_candidates:
            for rel in delete_candidates:
                if rel.on_delete.__name__ == 'CASCADE' and rel.one_to_many and not rel.hidden:
                    for item in getattr(self, rel.related_name).all():
                        item.delete()

        self.save(update_fields=['is_deleted', ])

    class Meta:
        abstract = True


class Post(IsDeletedMixin):

    MODERATION_CHOICES = [
        ('NOT_MODERATED', 'На модерацию'),
        ('VALID', 'Опубликовано'),
        ('INVALID', 'Отклонено'),
    ]
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.CharField(max_length=80, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    publicated_at = models.DateTimeField(verbose_name='Дата публикации', null=True, blank=True)

    moderation_status = models.CharField(
        max_length=100, blank=False,
        verbose_name='Статус модерации', choices=MODERATION_CHOICES, default='NOT_MODERATED'
    )
    publish = models.DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='post/images', verbose_name="Фото")
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name="Автор", related_name='author')
    liked = models.ManyToManyField('CustomUser', default=None, blank=True, related_name='liked')

    def __str__(self):
        return str(self.title)

    @property
    def num_like(self):
        return self.likes.all().count()


    @property
    def liked_users(self):
        return CustomUser.objects.filter(id__in=self.likes.values_list('user_id'))

    class Meta:
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('posts_detail', kwargs={'det': self.pk})
