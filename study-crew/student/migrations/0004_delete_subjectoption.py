# Generated by Django 5.2.1 on 2025-05-12 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_subjectoption_subject_unique_subject_per_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SubjectOption',
        ),
    ]
