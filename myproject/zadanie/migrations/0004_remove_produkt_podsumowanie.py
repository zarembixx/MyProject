# Generated by Django 5.0.7 on 2024-07-16 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zadanie', '0003_alter_produkt_cena_alter_produkt_podsumowanie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produkt',
            name='podsumowanie',
        ),
    ]
