# Generated by Django 4.2.7 on 2025-03-08 23:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0026_dropout_is_dropout"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dropout",
            name="is_dropout",
            field=models.BooleanField(default=True, verbose_name="Es Baja"),
        ),
    ]
