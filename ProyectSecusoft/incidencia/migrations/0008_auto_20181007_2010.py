# Generated by Django 2.0.7 on 2018-10-08 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0007_auto_20181007_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipoindicencia',
            name='asunto',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tipoindicencia',
            name='descripcion',
            field=models.TextField(max_length=200),
        ),
    ]