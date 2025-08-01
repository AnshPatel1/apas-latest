# Generated by Django 4.1.6 on 2023-02-18 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyFOET', '0023_rename_collaborator_collaboration_faculty_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foetassistantprofoncontractappraisalfile',
            old_name='involvement_extra_curricular_total',
            new_name='involvement_extra_curricular_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='evaluation_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='exam_duty_total_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='involvement_extra_curricular',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='modern_teaching_methods_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='paper_setting_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='part_a_section_2b_total',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='result_submission_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='teaching_load_marks',
        ),
        migrations.RemoveField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='timely_investigation_marks',
        ),
        migrations.AddField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='dissertation_total',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dissertation_total', to='FacultyFOET.markfield'),
        ),
        migrations.AddField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='phd_guidance_total',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phd_guidance_total', to='FacultyFOET.markfield'),
        ),
        migrations.AddField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='projects_total_marks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects_total_marks', to='FacultyFOET.markfield'),
        ),
        migrations.AlterField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='e_publications_articles',
            field=models.ManyToManyField(blank=True, related_name='e_publications_articles', to='FacultyFOET.paper'),
        ),
        migrations.AlterField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='industry_collaboration',
            field=models.ManyToManyField(blank=True, related_name='industry_collaboration', to='FacultyFOET.collaboration'),
        ),
        migrations.AlterField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='providing_consultancy',
            field=models.ManyToManyField(blank=True, related_name='providing_consultancy', to='FacultyFOET.consultancy'),
        ),
        migrations.CreateModel(
            name='TeachingLoad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2023)),
                ('semester_odd', models.FloatField(default=0)),
                ('semester_even', models.FloatField(default=0)),
                ('semester_third', models.FloatField(default=0)),
                ('marks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyFOET.markfield')),
            ],
        ),
        migrations.CreateModel(
            name='ExamDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2023)),
                ('timely_investigation', models.FloatField(blank=True, null=True)),
                ('paper_setting', models.FloatField(blank=True, null=True)),
                ('evaluation', models.FloatField(blank=True, null=True)),
                ('result_submission', models.FloatField(blank=True, null=True)),
                ('marks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FacultyFOET.markfield')),
            ],
        ),
        migrations.AddField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='exam_duty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exam_duty_total_marks', to='FacultyFOET.examduty'),
        ),
        migrations.AlterField(
            model_name='foetassistantprofoncontractappraisalfile',
            name='teaching_load',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaching_load', to='FacultyFOET.teachingload'),
        ),
    ]
