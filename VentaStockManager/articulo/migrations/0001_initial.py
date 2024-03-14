# Generated by Django 5.0.1 on 2024-02-29 12:21

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Articulo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=255)),
                ("descripcion", models.TextField()),
                ("precio_compra", models.DecimalField(decimal_places=2, max_digits=10)),
                ("precio_venta", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField()),
                (
                    "precio_minorista",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "precio_mayorista",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("vencimiento", models.DateField(blank=True)),
            ],
        ),
    ]