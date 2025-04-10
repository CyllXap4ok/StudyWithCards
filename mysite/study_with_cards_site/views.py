from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from study_with_cards_app.models import CardSet, Card
from .forms import UserSignInForm, UserSignUpForm

@login_required(login_url='sign_in')
def home_view(request):
    return render(request, 'home.html')

def signin_view(request):
    if request.method == 'POST':
        form = UserSignInForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Form validation error")
    else:
        form = UserSignInForm()

    return render(request, 'sign_in.html', {'form': form})

def signup_view(request):
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
    return render(request, 'cards_creation.html')

@login_required(login_url='sign_in')
def cards_study_view(request, cardset_id):
    cardset = get_object_or_404(CardSet, id=cardset_id, user=request.user)
    cards = cardset.card_set.all()
    return render(request, 'cards_study.html', {'cardset': cardset, 'cards': cards})

@login_required(login_url='sign_in')
def stats_view(request):
    return render(request, 'stats.html')

@login_required(login_url='sign_in')
def delete_cardset(request, cardset_id):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Требуется авторизация'})

    try:
        cardset = CardSet.objects.get(id=cardset_id, user=request.user)
        cardset.delete()
        return JsonResponse({'success': True})
    except CardSet.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Набор карточек не найден'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='sign_in')
@require_POST
def create_card_set(request):
    if request.method == 'POST':
        card_set_name = request.POST.get('card_set_name', 'Новый набор')

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
            Card.objects.create(
                card_set=card_set,
                term=term[0],  # Так как это список с одним элементом
                definition=definition[0]
            )

        return redirect('home')

    return redirect('cards_creation')
