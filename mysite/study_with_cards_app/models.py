from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import random

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


class CardSet(models.Model):
    COLORS = ['#7F56DA', '#22C55E', '#EA580C']
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    bg_color = models.CharField(max_length=7, default=COLORS[0])

    def save(self, *args, **kwargs):
        if not self.bg_color:
            self.bg_color = random.choice(self.COLORS)
        super().save(*args, **kwargs)


class Card(models.Model):
    card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    term = models.TextField()
    definition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
