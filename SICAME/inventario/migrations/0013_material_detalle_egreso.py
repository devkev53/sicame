# Generated by Django 2.2.5 on 2019-10-07 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_ingreso_is_baja'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material_Detalle_Egreso',
            fields=[
            ],
            options={
                'verbose_name': 'Egreso',
                'verbose_name_plural': 'Egresos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inventario.material_detalle',),
        ),
    ]
