# Generated by Django 4.2.2 on 2023-06-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upis', '0009_remove_uloga_naziv_uloge_uloga_uloga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmeti',
            name='izborni',
            field=models.CharField(choices=[('da', 'da'), ('ne', 'ne')], max_length=10),
        ),
    ]
