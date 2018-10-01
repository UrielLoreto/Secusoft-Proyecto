# Generated by Django 2.0.7 on 2018-09-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0010_auto_20180916_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='activo',
            new_name='active',
        ),
        migrations.AddField(
            model_name='usuario',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]