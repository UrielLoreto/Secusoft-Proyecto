# Generated by Django 2.0.7 on 2018-10-28 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_auto_20181027_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='grado',
            field=models.CharField(blank=True, choices=[('1', 'Primero'), ('2', 'Segundo'), ('3', 'Tercero')], max_length=10, null=True),
        ),
    ]
