# Generated by Django 2.0.7 on 2018-11-19 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cita', '0004_auto_20181118_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]