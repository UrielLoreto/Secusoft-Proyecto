# Generated by Django 2.0.7 on 2018-10-22 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20181021_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateField(default='1995-10-10'),
        ),
    ]
