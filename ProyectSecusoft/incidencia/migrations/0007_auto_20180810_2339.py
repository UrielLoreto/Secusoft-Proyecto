# Generated by Django 2.0.7 on 2018-08-11 04:39

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('cita', '0005_auto_20180728_2233'),
        ('usuario', '0007_auto_20180801_2017'),
        ('incidencia', '0006_auto_20180728_2233'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comentario_rel',
            new_name='ComentarioRel',
        ),
        migrations.RenameModel(
            old_name='Incidencia_alumno',
            new_name='IncidenciaAlumno',
        ),
        migrations.RenameModel(
            old_name='Incidencia_docente',
            new_name='IncidenciaCita',
        ),
        migrations.RenameModel(
            old_name='Incidencia_cita',
            new_name='IncidenciaDocente',
        ),
        migrations.RenameModel(
            old_name='Incidencia_padre',
            new_name='IncidenciaPadre',
        ),
        migrations.RemoveField(
            model_name='incidenciacita',
            name='docente',
        ),
        migrations.RemoveField(
            model_name='incidenciadocente',
            name='cita',
        ),
        migrations.AddField(
            model_name='incidenciacita',
            name='cita',
            field=models.ManyToManyField(blank=True, to='cita.Cita'),
        ),
        migrations.AddField(
            model_name='incidenciadocente',
            name='docente',
            field=models.ManyToManyField(blank=True, to='usuario.Docente'),
        ),
    ]