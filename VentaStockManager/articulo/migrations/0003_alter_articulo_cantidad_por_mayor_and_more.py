# Generated by Django 4.2 on 2024-05-11 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articulo', '0002_articulo_cantidad_por_mayor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='cantidad_por_mayor',
            field=models.PositiveIntegerField(default=100, null=True),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='precio_mayorista',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='precio_minorista',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]