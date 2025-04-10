"""Backend модуль"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    """Класс предоставляющий кастомный бэкэнд для аутентификации"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Функция для аутентификации пользователя.
           Аутентифицирует по email вместо username, установленного по-умолчанию.
        """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None
