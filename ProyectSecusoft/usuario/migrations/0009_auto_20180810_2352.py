# Generated by Django 2.0.7 on 2018-08-11 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_auto_20180810_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='correo',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]