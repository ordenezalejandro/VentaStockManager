# Generated by Django 4.2.13 on 2024-05-30 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("articulo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Compra",
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
            ],
        ),
        migrations.CreateModel(
            name="Proveedor",
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
                ("nombre", models.CharField(max_length=255)),
                ("apellido", models.CharField(max_length=255)),
                ("direccion", models.CharField(blank=True, max_length=255, null=True)),
                ("telefono", models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="DetalleCompra",
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
                ("cantidad", models.PositiveIntegerField(default=1)),
                (
                    "precio_unitario",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "articulo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articulos_comprados",
                        to="articulo.articulo",
                    ),
                ),
                (
                    "compra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles_compra",
                        to="compra.compra",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="compra",
            name="proveedor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="compra.proveedor"
            ),
        ),
    ]