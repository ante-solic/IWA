# Generated by Django 4.2.1 on 2023-06-09 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upis', '0004_alter_uloga_naziv_uloge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upisi',
            old_name='korisnik_id',
            new_name='korisnik',
        ),
        migrations.RenameField(
            model_name='upisi',
            old_name='predmet_id',
            new_name='predmet',
        ),
    ]