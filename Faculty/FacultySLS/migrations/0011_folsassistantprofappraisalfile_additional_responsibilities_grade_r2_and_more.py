# Generated by Django 4.1.5 on 2023-06-08 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacultySLS', '0010_folsassistantprofappraisalfile_r1_grade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='folsassistantprofappraisalfile',
            name='additional_responsibilities_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassistantprofappraisalfile',
            name='self_development_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassistantprofappraisalfile',
            name='senior_feedback_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassistantprofoncontractappraisalfile',
            name='additional_responsibilities_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassistantprofoncontractappraisalfile',
            name='self_development_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassistantprofoncontractappraisalfile',
            name='senior_feedback_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassociateprofappraisalfile',
            name='additional_responsibilities_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassociateprofappraisalfile',
            name='self_development_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsassociateprofappraisalfile',
            name='senior_feedback_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsprofappraisalfile',
            name='additional_responsibilities_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsprofappraisalfile',
            name='self_development_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='folsprofappraisalfile',
            name='senior_feedback_grade_r2',
            field=models.CharField(blank=True, choices=[('O', 'Outstanding'), ('G', 'Good'), ('A', 'Average'), ('U', 'Unsatisfactory')], max_length=1, null=True),
        ),
    ]
