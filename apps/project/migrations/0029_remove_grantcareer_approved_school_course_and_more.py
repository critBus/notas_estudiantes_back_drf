# Generated by Django 4.2.7 on 2025-03-16 18:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0028_student_can_edit_bullet"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="grantcareer",
            name="approved_school_course",
        ),
        migrations.AddField(
            model_name="grantcareer",
            name="school_year",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="project.schoolyear",
                verbose_name="Año escolar",
            ),
            preserve_default=False,
        ),
    ]
