# Generated by Django 4.2.13 on 2024-06-07 00:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cliente", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="apellido",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="direccion",
            field=models.CharField(blank=True, default="direccion", max_length=50),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="telefono",
            field=models.TextField(blank=True, default="00000000"),
        ),
    ]