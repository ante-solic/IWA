# Generated by Django 4.2.1 on 2023-06-09 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upis', '0002_alter_predmeti_nositelj_predmeta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='upisi',
            old_name='student_id',
            new_name='korisnik_id',
        ),
        migrations.AddField(
            model_name='upisi',
            name='status',
            field=models.CharField(blank=True, choices=[('not', 'Neupisan'), ('enr', 'Upisan'), ('pass', 'Polozen')], max_length=50, null=True),
        ),
    ]
