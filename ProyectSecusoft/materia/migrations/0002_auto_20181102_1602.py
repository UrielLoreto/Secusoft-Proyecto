# Generated by Django 2.0.7 on 2018-11-02 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiadocente',
            name='docente',
            field=models.ManyToManyField(blank=True, null=True, to='usuario.Docente'),
        ),
    ]
