# Generated by Django 2.2.5 on 2019-09-14 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asignacion', '0005_auto_20190913_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material_asig',
            name='ref_ingreso',
        ),
        migrations.RemoveField(
            model_name='material_asig',
            name='ubicacion',
        ),
    ]