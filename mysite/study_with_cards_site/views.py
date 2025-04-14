"""Модуль views для приложения study_with_cards_app.

Содержит view-функции для обработки запросов:
- Аутентификация и регистрация пользователей
- Работа с наборами карточек
- Просмотр статистики

Все страницы доступны только авторизованным пользователям,
кроме: sing_in и sign_up
"""

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from study_with_cards_app.models import CardSet, Card
from .forms import UserSignInForm, UserSignUpForm


@login_required(login_url='sign_in')
def home_view(request):
    """Главная страница.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse: Рендер шаблона home.html.
    """
    return render(request, 'home.html')


def signin_view(request):
    """Страница логина.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse:
            - При успешной аутентификации - редирект на главную
            - При ошибке - рендер формы входа с сообщениями об ошибках
    """
    if request.method == 'POST':
        form = UserSignInForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Form validation error")
    else:
        form = UserSignInForm()

    return render(request, 'sign_in.html', {'form': form})


def signup_view(request):
    """Страница регистрации.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse:
            - При успешной регистрации - редирект на страницу входа
            - При ошибке - рендер формы регистрации
    """
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    else:
        form = UserSignUpForm()

    return render(request, 'sign_up.html', {'form': form})


@login_required(login_url='sign_in')
def cards_creation_view(request):
    """Страница создания новых карточек.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse: Рендер шаблона cards_creation.html.
    """
    return render(request, 'cards_creation.html')


def get_card_html(request):
    """Функция, предоставляющая шаблон карточки (для JS)"""
    html = render_to_string('inner_templates/card.html')
    return HttpResponse(html)


@login_required(login_url='sign_in')
def cards_study_view(request, cardset_id):
    """Страница изучения карточек из конкретного набора.

    Args:
        request: HttpRequest объект.
        cardset_id: ID набора карточек.

    Returns:
        HttpResponse: Рендер шаблона cards_study.html с контекстом:
            - cardset: Набор карточек
            - cards: Карточки из набора

    Raises:
        404: Если набор не существует или не принадлежит пользователю.
    """
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    cards = cardset.card_set.all()
    return render(request, 'cards_study.html', {'cardset': cardset, 'cards': cards})


@login_required(login_url='sign_in')
def stats_view(request):
    """Страница просмотра статистики.

    Args:
        request: HttpRequest объект.

    Returns:
        HttpResponse: Рендер шаблона stats.html.
    """
    return render(request, 'stats.html')


@login_required(login_url='sign_in')
def delete_cardset(request, cardset_id):
    """Удаление набора карточек.

    Args:
        request: HttpRequest объект.
        cardset_id: ID набора карточек для удаления.

    Returns:
        HttpResponse: Редирект на главную страницу.

    Raises:
        404: Если набор не существует или не принадлежит пользователю.
    """
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    cardset.delete()
    return redirect('home')


@login_required(login_url='sign_in')
@require_POST
def create_card_set(request):
    """Создание нового набора карточек.

    Обрабатывает POST-запрос с данными карточек.

    Args:
        request: HttpRequest объект (только POST).

    Returns:
        HttpResponse:
            - При успешном создании - редирект на главную
            - При ошибке - редирект на страницу создания карточек
    """
    if request.method == 'POST':
        card_set_name = request.POST.get('card_set_name', 'Новый набор')

        if not card_set_name: return redirect('cards_creation')

        card_set = CardSet.objects.create(
            user=request.user,
            name=card_set_name
        )

        # Получаем все поля, начинающиеся с 'term_' или 'definition_'
        post_data = dict(request.POST)
        terms = [v for k, v in post_data.items() if k.startswith('term_')]
        definitions = [v for k, v in post_data.items() if k.startswith('definition_')]

        # Создаем карточки, объединяя термины и определения
        for term, definition in zip(terms, definitions):
            if term is None or definition is None: break
            Card.objects.create(
                card_set=card_set,
                term=term[0],
                definition=definition[0]
            )

        return redirect('home')

    return redirect('cards_creation')
