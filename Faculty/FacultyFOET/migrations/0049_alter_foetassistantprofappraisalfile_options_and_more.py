# Generated by Django 4.1.6 on 2023-03-20 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyFOET', '0048_foetgoalsheetassistantprof_section_2b_phd_guidance_external_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foetassistantprofappraisalfile',
            options={'verbose_name': 'FoET Assistant Professor On Contract Appraisal File', 'verbose_name_plural': 'FoET Assistant Professor On Contract Appraisal Files'},
        ),
        migrations.AlterModelOptions(
            name='foetassociateprofappraisalfile',
            options={'verbose_name': 'FoET Associate Professor Appraisal File', 'verbose_name_plural': 'FoET Associate Professor Appraisal Files'},
        ),
        migrations.AlterModelOptions(
            name='foetprofappraisalfile',
            options={'verbose_name': 'FoET Professor Appraisal File', 'verbose_name_plural': 'FoET Professor Appraisal Files'},
        ),
    ]
