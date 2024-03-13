# Generated by Django 5.0.3 on 2024-03-09 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("articulo", "0001_initial"),
        ("cliente", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Venta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fecha_compra", models.DateField()),
                ("fecha_entrega", models.DateField()),
                (
                    "cliente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ventas",
                        to="cliente.cliente",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ArticuloVenta",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.PositiveBigIntegerField()),
                (
                    "precio_minorista",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "precio_mayorista",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "articulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articulos_ventdidos",
                        to="articulo.articulo",
                    ),
                ),
                (
                    "venta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ventas",
                        to="venta.venta",
                    ),
                ),
            ],
        ),
    ]
