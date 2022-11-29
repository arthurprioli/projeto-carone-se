# Generated by Django 4.1.1 on 2022-11-29 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("office", "0008_remove_carona_passageiros_usuario_carona"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="carona",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="office.carona",
            ),
        ),
    ]
