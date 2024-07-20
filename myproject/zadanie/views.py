from django.shortcuts import render, get_object_or_404, redirect
from .models import Zadanie
from .forms import ZadanieForm, ZadanieFilterForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponse
def zadanie_opis_widok(request):
    form = ZadanieFilterForm(request.GET or None)
    zadania = Zadanie.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['id']:
            zadania = zadania.filter(id=form.cleaned_data['id'])
        if form.cleaned_data['nazwa']:
            zadania = zadania.filter(nazwa__icontains=form.cleaned_data['nazwa'])
        if form.cleaned_data['opis']:
            zadania = zadania.filter(opis__icontains=form.cleaned_data['opis'])
        if form.cleaned_data['status']:
            zadania = zadania.filter(status=form.cleaned_data['status'])
        if form.cleaned_data['uzytkownik']:
            zadania = zadania.filter(przypisany_uzytkownik=form.cleaned_data['uzytkownik'])
    
    can_edit_all_tasks = request.user.has_perm('zadanie.can_edit_all_tasks')
    
    return render(request, 'zadanie/opis.html', {
        'form': form,
        'zadania': zadania,
        'can_edit_all_tasks': can_edit_all_tasks,
    })

@login_required
def zadanie_edytuj_widok(request, pk):
    zadanie = get_object_or_404(Zadanie, pk=pk)
    if request.user == zadanie.przypisany_uzytkownik or request.user.has_perm('zadanie.can_edit_all_tasks'):
        if request.method == 'POST':
            form = ZadanieForm(request.POST, instance=zadanie, user=request.user)
            if form.is_valid():
                zadanie = form.save(commit=False)
                if not request.user.has_perm('zadanie.can_edit_all_tasks'):
                    zadanie.przypisany_uzytkownik = zadanie._state.fields_cache['przypisany_uzytkownik']
                zadanie.save()
                return redirect('zadania_szczegoly', pk=zadanie.pk)
        else:
            form = ZadanieForm(instance=zadanie, user=request.user)
        return render(request, 'zadanie/edytuj.html', {'form': form})
    else:
        return redirect('home')  # Lub inna strona, jeśli użytkownik nie ma uprawnień

    
@login_required
@permission_required('zadanie.can_delete_users', raise_exception=True)
def usun_uzytkownika(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        # Usuń użytkownika i zaktualizuj zadania
        zadania = Zadanie.objects.filter(przypisany_uzytkownik=user)
        for zadanie in zadania:
            zadanie.przypisany_uzytkownik = None
            zadanie.save()
        user.delete()
        return redirect('moje_konto')  # Przekierowanie na stronę "Moje Konto" po usunięciu użytkownika
    return render(request, 'zadanie/usun_uzytkownika.html', {'user': user})

def usun_zadania_widok(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('zadania')
        if selected_ids:
            Zadanie.objects.filter(pk__in=selected_ids).delete()
    return redirect('home')

def zadania_szczegoly(request, pk):
    zadania = get_object_or_404(Zadanie, pk=pk)
    return render(request, 'zadanie/szczegoly.html', {'zadania': zadania})

@login_required
def zadanie_dodaj_widok(request):
    if request.method == 'POST':
        form = ZadanieForm(request.POST)
        form.request = request  # Ustawienie request na formularzu
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ZadanieForm()
        form.request = request  # Ustawienie request na formularzu
    return render(request, 'zadanie/dodaj.html', {'form': form})


def zadanie_historia_widok(request, ids):
    zadanie_ids = ids.split(',')
    zadania = Zadanie.objects.filter(pk__in=zadanie_ids)
    historie = []
    for zadanie in zadania:
        historia = zadanie.history.all()
        zmiany = []
        for i in range(len(historia) - 1):
            current = historia[i]
            previous = historia[i + 1]
            changes = current.diff_against(previous).changes
            updated_changes = []
            for change in changes:
                if change.field == 'uzytkownik':
                    old_user = User.objects.get(pk=change.old).username if change.old else "Brak użytkownika"
                    new_user = User.objects.get(pk=change.new).username if change.new else "Brak użytkownika"
                    updated_changes.append({
                        'field': change.field,
                        'old': old_user,
                        'new': new_user
                    })
                else:
                    updated_changes.append({
                        'field': change.field,
                        'old': change.old,
                        'new': change.new
                    })
            zmiany.append((current, updated_changes))
        if historia:
            zmiany.append((historia.last(), []))
        historie.append((zadanie, zmiany))
    return render(request, 'zadanie/historia.html', {'historie': historie})
@login_required
def wybierz_zadania_widok(request):
    zadania = Zadanie.objects.all()
    can_edit_all_tasks = request.user.has_perm('zadanie.can_edit_all_tasks')
    if request.method == 'POST':
        selected_ids = request.POST.getlist('zadania')
        if 'usun' in request.POST:
            Zadanie.objects.filter(id__in=selected_ids).delete()
            return redirect('home')
        elif 'historia' in request.POST:
            return redirect('zadanie_historia', ids=','.join(selected_ids))
    return render(request, 'zadanie/wybierz_zadania.html', {'zadania': zadania, 'can_edit_all_tasks': can_edit_all_tasks})

def reset_auto_increment():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='zadanie_zadanie';")

def reset_id_view(request):
    reset_auto_increment()
    return HttpResponse("Autoinkrementacja została zresetowana.")


@login_required
def moje_konto(request):
    zadania = Zadanie.objects.filter(przypisany_uzytkownik=request.user)
    wszyscy_uzytkownicy = User.objects.all() if request.user.is_superuser or request.user.has_perm('zadanie.can_delete_users') else None
    can_edit_all_tasks = request.user.has_perm('zadanie.can_edit_all_tasks')
    return render(request, 'zadanie/moje_konto.html', {
        'zadania': zadania,
        'wszyscy_uzytkownicy': wszyscy_uzytkownicy,
        'can_edit_all_tasks': can_edit_all_tasks
    })
@login_required
def usun_konto(request):
    user = request.user
    if request.method == "POST":
        # Usuń użytkownika i zaktualizuj zadania
        zadania = Zadanie.objects.filter(przypisany_uzytkownik=user)
        for zadanie in zadania:
            zadanie.uzytkownik = None
            zadanie.save()
        user.delete()
        return redirect('home')  # Przekierowanie na stronę główną po usunięciu konta
    return render(request, 'zadanie/usun_konto.html')