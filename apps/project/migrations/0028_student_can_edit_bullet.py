# Generated by Django 4.2.7 on 2025-03-09 22:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0027_alter_dropout_is_dropout"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="can_edit_bullet",
            field=models.BooleanField(
                default=False, verbose_name="Puede Editar Su Boleta"
            ),
        ),
    ]
