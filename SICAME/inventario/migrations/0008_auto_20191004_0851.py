# Generated by Django 2.2.5 on 2019-10-04 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('inventario', '0007_auto_20191003_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipo_ingreso',
            name='categ',
        ),
        migrations.RemoveField(
            model_name='equipo_ingreso',
            name='orden',
        ),
        migrations.AddField(
            model_name='equipo_ingreso',
            name='id_Marca',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Marca', verbose_name='Marca'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipo_ingreso',
            name='modelo',
            field=models.CharField(default=1, max_length=25, verbose_name='Orden'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipo_ingreso',
            name='serie',
            field=models.CharField(default=1, max_length=25, verbose_name='Orden'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipo_ingreso',
            name='monto',
            field=models.DecimalField(decimal_places=1, max_digits=12, verbose_name='Precio Unidad'),
        ),
    ]