# Generated by Django 4.1.6 on 2023-04-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyScience', '0005_scienceassistantprofappraisalfile_faculty_advisor_available_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scienceassistantprofappraisalfile',
            name='is_assistant_prof_on_contract',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scienceassociateprofappraisalfile',
            name='is_assistant_prof_on_contract',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scienceprofappraisalfile',
            name='is_assistant_prof_on_contract',
            field=models.BooleanField(default=False),
        ),
    ]
