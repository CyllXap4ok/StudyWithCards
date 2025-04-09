from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Бэкенд вызван!")  # Проверка
        try:
            user = User.objects.get(email=username)
            print("Найден пользователь:", user)  # Проверка
            if user.check_password(password):
                print("Пароль верный!")  # Проверка
                return user
            else:
                print("Неверный пароль!")  # Проверка
                return None

        except User.DoesNotExist:
            print("Пользователь не найден!")
            return None
        except User.MultipleObjectsReturned:
            return None