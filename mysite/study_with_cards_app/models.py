from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'avatars/{uuid.uuid4()}.{ext}'

class User(AbstractUser):
    username = None  # Убираем стандартное поле username
    email = models.EmailField(_('email address'), unique=True, blank=False)  # Основной идентификатор
    name = models.CharField(_('name'), max_length=30, blank=False)

    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Указываем поле для аутентификации
    REQUIRED_FIELDS = ['name']  # Обязательные поля при createsuperuser

    def __str__(self):
        return self.email
