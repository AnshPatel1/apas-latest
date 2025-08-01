# Generated by Django 4.1.5 on 2023-05-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyScience', '0007_rename_section_1e_iii_per_international_book_per_author_sciencegoalsheetassistantprof_section_1e_ii_'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultyvalidator',
            name='academia_collab_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facultyvalidator',
            name='award_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facultyvalidator',
            name='extra_curricular_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facultyvalidator',
            name='project_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facultyvalidator',
            name='research_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facultyvalidator',
            name='senior_feedback_validated',
            field=models.BooleanField(default=False),
        ),
    ]
