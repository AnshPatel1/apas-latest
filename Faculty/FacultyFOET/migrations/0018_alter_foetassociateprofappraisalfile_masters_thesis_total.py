# Generated by Django 4.1.6 on 2023-02-14 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyFOET', '0017_alter_foetassistantprofappraisalfile_academia_collaboration_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foetassociateprofappraisalfile',
            name='masters_thesis_total',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assoc_prof_masters_thesis_total', to='FacultyFOET.markfield'),
        ),
    ]
