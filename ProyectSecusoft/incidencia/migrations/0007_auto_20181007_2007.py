# Generated by Django 2.0.7 on 2018-10-08 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencia', '0006_auto_20181007_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidencia',
            name='asunto',
        ),
        migrations.AddField(
            model_name='tipoindicencia',
            name='asunto',
            field=models.CharField(default='holi', max_length=200),
            preserve_default=False,
        ),
    ]