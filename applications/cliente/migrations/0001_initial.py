# Generated by Django 5.0.6 on 2024-09-30 22:04

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('numero_documento', models.CharField(max_length=13, verbose_name='RUC')),
                ('tipo_persona', models.CharField(choices=[('0', 'Persona Natural'), ('1', 'Persona Juridica')], max_length=2, verbose_name='Tipo Persona')),
                ('tipo_documento', models.CharField(choices=[('0', 'DNI'), ('1', 'RUC'), ('2', 'Pasaporte'), ('3', 'Carnet Extranjeria')], max_length=2, verbose_name='Tipo Documento')),
                ('direccion', models.CharField(max_length=100, verbose_name='Direccion')),
                ('telefono', models.CharField(max_length=10, verbose_name='Telefono')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('contacto', models.CharField(max_length=70, verbose_name='Contacto')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('anulado', models.BooleanField(default=True, verbose_name='Estado')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
