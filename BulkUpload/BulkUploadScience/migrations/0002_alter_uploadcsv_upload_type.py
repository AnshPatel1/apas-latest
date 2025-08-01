# Generated by Django 4.1.6 on 2023-03-20 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BulkUploadScience', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadcsv',
            name='upload_type',
            field=models.CharField(choices=[('additional', 'Additional Marks (Placement & Admission'), ('co_curricular', 'Co-Curricular Activities'), ('academia_collab', 'Academia Collaboration'), ('award', 'Awards'), ('patent', 'Patent'), ('phd_guidance', 'PhD Guidance'), ('project', 'Project'), ('scopus_wos', 'Paper Publications in Scopus & Web of Science'), ('books', 'Books and Publications'), ('exam_duty', 'Exam Duty'), ('student_feedback', 'Student Feedback'), ('teaching_load', 'Teaching Load')], max_length=100),
        ),
    ]
