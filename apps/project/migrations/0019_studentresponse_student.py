# Generated by Django 4.2.7 on 2025-02-28 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "project",
            "0018_alter_filefolder_file_alter_fileschooltask_file_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="studentresponse",
            name="student",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="project.student",
                verbose_name="Estudiante",
            ),
            preserve_default=False,
        ),
    ]
