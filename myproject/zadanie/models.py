from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# Create your models here.


class Zadanie(models.Model):
    STATUS_CHOICES = (
        ('new', 'Nowy'),
        ('in_progress', 'W toku'),
        ('resolved', 'Rozwiązany'),
    )
    nazwa = models.CharField(max_length=250)
    opis = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
    )
    przypisany_uzytkownik = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    history = HistoricalRecords()
    class Meta:
        permissions = [
            ("can_edit_all_tasks", "Can edit all tasks"),
            ("can_delete_users", "Can delete users"),
        ]
    def __str__(self):
        return self.nazwa