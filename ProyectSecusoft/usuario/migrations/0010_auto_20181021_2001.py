# Generated by Django 2.0.7 on 2018-10-22 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_usuario_fecha_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
