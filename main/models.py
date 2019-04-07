from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField


class User(AbstractUser):
    USER_SIMPLE = 1
    USER_MODERATOR = 2

    USER_CHOICES = (
        (USER_SIMPLE, _('Пользователь')),
        (USER_MODERATOR, _('Модератор')),
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_CHOICES,
        default=USER_SIMPLE,
        verbose_name=_('Тип пользователя')
    )

    @property
    def is_simple_user(self):
        return self.user_type == User.USER_SIMPLE

    @property
    def is_moderator(self):
        return self.user_type == User.USER_MODERATOR

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Название'))

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name


class Record(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name=_('Наименование записи'))

    content = HTMLField(blank=True, verbose_name=_('Контент'))

    date_created = models.DateTimeField(default=timezone.now, verbose_name=_('Дата создания'))

    date_modified = models.DateTimeField(default=timezone.now, verbose_name=_('Дата изменения'))

    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Теги'),
        blank=True,
        related_name='records',
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
        blank=True,
        null=True,
        related_name='records'
    )

    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Кем изменено'),
        blank=True,
        null=True,
        related_name='modifications'
    )

    class Meta:
        verbose_name = _('Запись')
        verbose_name_plural = _('Записи')

    @cached_property
    def stripped_content(self):
        return strip_tags(self.content)

    def __str__(self):
        return self.stripped_content[:64]
