# Generated by Django 2.0.7 on 2018-08-11 04:39

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('incidencia', '0007_auto_20180810_2339'),
        ('usuario', '0007_auto_20180801_2017'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Padre_Alumno',
            new_name='PadreAlumno',
        ),
        migrations.RenameModel(
            old_name='Padre_Familia',
            new_name='PadreFamilia',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='nivel',
        ),
    ]
