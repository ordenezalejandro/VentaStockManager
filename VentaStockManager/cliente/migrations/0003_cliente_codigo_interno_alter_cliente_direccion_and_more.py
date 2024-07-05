# Generated by Django 4.2.13 on 2024-07-05 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cliente", "0002_alter_cliente_apellido_alter_cliente_direccion_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="codigo_interno",
            field=models.CharField(
                blank=True, default="no-codigo", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="direccion",
            field=models.CharField(
                blank=True, default="direccion", max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="telefono",
            field=models.TextField(blank=True, default="00000000", null=True),
        ),
    ]
