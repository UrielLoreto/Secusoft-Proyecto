# Generated by Django 2.0.7 on 2018-09-30 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_auto_20180930_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='MateriaDocente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docente', models.ManyToManyField(to='usuario.Docente')),
                ('materia', models.ManyToManyField(to='usuario.Materia')),
            ],
        ),
    ]
