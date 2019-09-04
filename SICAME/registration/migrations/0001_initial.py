# Generated by Django 2.2.5 on 2019-09-04 20:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import registration.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to=registration.models.custom_upload_to)),
                ('direccion', models.CharField(blank=True, max_length=50, verbose_name='Direccion')),
                ('telefono', models.CharField(blank=True, max_length=8, validators=[django.core.validators.RegexValidator(message='Ingrese solamente numeros', regex='^[0-9]*$'), registration.models.val_tel], verbose_name='Telefono')),
                ('puesto', models.CharField(blank=True, max_length=25, verbose_name='Puesto')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Perfile',
                'verbose_name_plural': 'Perfiles',
            },
        ),
    ]
