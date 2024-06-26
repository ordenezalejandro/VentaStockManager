# Generated by Django 4.2.13 on 2024-05-30 03:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
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
                ("nombre", models.TextField()),
                ("apellido", models.TextField(blank=True)),
                ("telefono", models.TextField(blank=True, null=True)),
                ("direccion", models.CharField(blank=True, max_length=50)),
            ],
            options={
                "verbose_name": "cliente",
                "verbose_name_plural": "clientes",
            },
        ),
    ]
