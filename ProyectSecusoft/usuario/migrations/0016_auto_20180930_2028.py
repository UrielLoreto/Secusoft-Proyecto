# Generated by Django 2.0.7 on 2018-10-01 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0015_materiadocente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materiadocente',
            name='docente',
        ),
        migrations.RemoveField(
            model_name='materiadocente',
            name='materia',
        ),
        migrations.DeleteModel(
            name='Materia',
        ),
        migrations.DeleteModel(
            name='MateriaDocente',
        ),
    ]
