# Generated by Django 2.0.7 on 2018-11-19 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cita', '0005_cita_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='descripcion',
        ),
    ]