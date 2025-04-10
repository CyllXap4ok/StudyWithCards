"""
URL configuration for study_with_cards_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cards/delete/<int:cardset_id>/', views.delete_cardset, name='delete_cardset'),
    path('signin/', views.signin_view, name='sign_in'),
    path('signup/', views.signup_view, name='sign_up'),
    path('cards_creation/', views.cards_creation_view, name='cards_creation'),
    path('cards_study/<int:cardset_id>/', views.cards_study_view, name='cards_study'),
    path('stats/', views.stats_view, name='stats'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_card_set', views.create_card_set, name='create_card_set')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
