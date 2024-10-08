# Generated by Django 5.0.6 on 2024-09-30 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_producto_num_purchase'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='average_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='Costo Promedio'),
        ),
    ]
