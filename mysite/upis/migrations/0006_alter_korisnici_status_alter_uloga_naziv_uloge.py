# Generated by Django 4.2.1 on 2023-06-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upis', '0005_rename_korisnik_id_upisi_korisnik_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korisnici',
            name='status',
            field=models.CharField(blank=True, choices=[('none', 'None'), ('izv', 'izvanredni'), ('red', 'redovni')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='uloga',
            name='naziv_uloge',
            field=models.CharField(choices=[('student', 'Student'), ('profesor', 'Profesor'), ('administrator', 'Administrator')], max_length=50),
        ),
    ]
