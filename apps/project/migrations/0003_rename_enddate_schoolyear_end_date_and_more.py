# Generated by Django 4.2.7 on 2025-02-11 21:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0002_schoolyear_remove_award_date_created_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="schoolyear",
            old_name="endDate",
            new_name="end_date",
        ),
        migrations.RenameField(
            model_name="schoolyear",
            old_name="startDate",
            new_name="start_date",
        ),
    ]
