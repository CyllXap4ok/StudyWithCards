"""Модуль форм для аутентификации в приложении study_with_cards_app.

   Содержит Django-формы для работы с пользователями:
   - Форма входа
   - Форма регистрации с дополнительными полями
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from study_with_cards_app.models import User


class UserSignInForm(AuthenticationForm):
    """Кастомная форма аутентификации пользователя.

    Расширяет стандартную AuthenticationForm, используя email в качестве логина
    и добавляя кастомные атрибуты полей.

    Attrs:
        username (EmailField): Поле для ввода email с подсказкой и автозаполнением.
        password (CharField): Поле для ввода пароля с маскировкой и автозаполнением.
    """
    username = forms.EmailField(
        label="Login",
        widget=forms.EmailInput(attrs={
            'autocomplete': 'email',
            'placeholder': 'email@email.com'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password'
        }),
        strip=False
    )


class UserSignUpForm(UserCreationForm):
    """Кастомная форма регистрации пользователя с дополнительными полями.

    Расширяет стандартную UserCreationForm, добавляя поля email, имя и аватар.
    Содержит дополнительную валидацию паролей и логику сохранения.

    Атрибуты:
        avatar (ImageField): Необязательное поле для загрузки аватара (png/jpeg).
        email (EmailField): Обязательное поле email с подсказкой.
        name (CharField): Обязательное поле имени.
        password1 (CharField): Поле для ввода пароля.
        password2 (CharField): Поле для подтверждения пароля.
    """
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'image/png, image/jpeg'
        })
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@email.com',
            'autocomplete': 'email'
        })
    )
    name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'your name'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={}),
        strip=False
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={}),
        strip=False
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'avatar')

    def clean_password2(self):
        """Проверка совпадения введенных паролей.

        Исключения:
            ValidationError: Если пароли не совпадают.

        Возвращает:
            str: Валидный пароль при успешной проверке.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        """Сохранение пользователя с хэшированием пароля.

        Аргументы:
            commit: Флаг немедленного сохранения в базу данных.

        Возвращает:
            User: Созданный экземпляр пользователя.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Хэшируем пароль
        if commit:
            user.save()
        return user
