# Generated by Django 2.2.5 on 2019-10-03 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_auto_20191003_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipo',
            options={'ordering': ['nombre'], 'verbose_name': 'Equipo', 'verbose_name_plural': 'Equipos'},
        ),
        migrations.AlterUniqueTogether(
            name='equipo',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='cat',
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='id_e',
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='identificador',
        ),
        migrations.RemoveField(
            model_name='equipo',
            name='orden',
        ),
    ]
