# Generated by Django 5.0.3 on 2024-03-23 19:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("vendedor", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendedor",
            name="apellido",
        ),
        migrations.RemoveField(
            model_name="vendedor",
            name="nombre",
        ),
    ]
