# Generated by Django 4.2.7 on 2025-02-23 17:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0013_professor_user_student_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="professor",
            name="grade",
        ),
    ]
