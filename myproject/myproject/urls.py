"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from zadanie import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.zadanie_opis_widok, name='home'),
    path('edytuj/<int:pk>/', views.zadanie_edytuj_widok, name='zadanie_edytuj'),
    path('usun_zadania/', views.usun_zadania_widok, name='usun_zadania'),
    path('accounts/', include('accounts.urls')),
    path('szczegoly/<int:pk>/', views.zadania_szczegoly, name='zadania_szczegoly'),
    path('dodaj/', views.zadanie_dodaj_widok, name='zadanie_dodaj'),
    path('historia/<str:ids>/', views.zadanie_historia_widok, name='zadanie_historia'),
    path('wybierz_zadania/', views.wybierz_zadania_widok, name='wybierz_zadania'),
    path('reset_id/', views.reset_id_view, name='reset_id'),
    path('moje_konto/', views.moje_konto, name='moje_konto'),
    path('usun_konto/', views.usun_konto, name='usun_konto'),
     path('usun_uzytkownika/<int:user_id>/', views.usun_uzytkownika, name='usun_uzytkownika'),
]
