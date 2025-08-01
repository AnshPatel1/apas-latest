# Generated by Django 4.1.5 on 2023-05-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacultySoEM', '0008_rename_section_4a_attending_conferences_marks_per_conference_foemgoalsheetassistantprof_section_4a_a'),
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
