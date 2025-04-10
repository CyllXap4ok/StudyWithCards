"""Модуль с моделями для базы данных"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def user_avatar_path(_, filename):
    """Сохраняет выбранный пользователем аватар в media/avatars/"""
    ext = filename.split('.')[-1]
    return f'avatars/{uuid.uuid4()}.{ext}'


class User(AbstractUser):
    """Модель для представления пользователя системы.

    Args:
        username - стандартное поле для аутентификации
        email - почта пользователя
        name - имя пользователя в свободном формате
        avatar - путь к аватару, сохраненному на сервере
    """
    username = None  # Убираем стандартное поле username
    email = models.EmailField(_('email address'), unique=True, blank=False)
    name = models.CharField(_('name'), max_length=30, blank=False)

    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Указываем поле для аутентификации
    REQUIRED_FIELDS = ['name']  # Обязательные поля при createsuperuser


class CardSet(models.Model):
    """Модель для представления набора карточек пользователя системы.

    Args:
        user - связанный с набором пользователь
        name - название набора карточек
        created_at - точное время создания набора
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Card(models.Model):
    """Модель для представления отдельных карточек набора.

    Args:
        card_set - связанный с карточкой набор
        term - термин (выводится на передней стороне)
        definition - определение (выводится на оборотной стороне)
        created_at - точное время создания набора
    """
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    term = models.CharField(max_length=50)
    definition = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
