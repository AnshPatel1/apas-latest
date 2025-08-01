# Generated by Django 4.1.6 on 2023-03-20 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FacultySoEM', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foemassistantprofappraisalfile',
            options={'verbose_name': 'FoEM Assistant Professor Appraisal File', 'verbose_name_plural': 'FoEM Assistant Professor Appraisal Files'},
        ),
        migrations.AlterModelOptions(
            name='foemassociateprofappraisalfile',
            options={'verbose_name': 'FoEM Associate Professor Appraisal File', 'verbose_name_plural': 'FoEM Associate Professor Appraisal Files'},
        ),
        migrations.AlterModelOptions(
            name='foemgoalsheetassistantprof',
            options={'verbose_name': 'Goalsheet Configuration for FoEM Assistant Professor On Contract', 'verbose_name_plural': 'Goalsheet Configurations for FoEM Assistant Professor On Contract'},
        ),
        migrations.AlterModelOptions(
            name='foemgoalsheetassistantprofoncontract',
            options={'verbose_name': 'Goalsheet Configuration for FoEM Assistant Professor On Contract', 'verbose_name_plural': 'Goalsheet Configurations for FoEM Assistant Professor On Contract'},
        ),
        migrations.AlterModelOptions(
            name='foemgoalsheetassociateprof',
            options={'verbose_name': 'Goalsheet Configuration for FoEM Assistant Professor On Contract', 'verbose_name_plural': 'Goalsheet Configurations for FoEM Assistant Professor On Contract'},
        ),
        migrations.AlterModelOptions(
            name='foemgoalsheetprof',
            options={'verbose_name': 'Goalsheet Configuration for FoEM Assistant Professor On Contract', 'verbose_name_plural': 'Goalsheet Configurations for FoEM Assistant Professor On Contract'},
        ),
        migrations.AlterModelOptions(
            name='foemprofappraisalfile',
            options={'verbose_name': 'FoEM Professor Appraisal File', 'verbose_name_plural': 'FoEM Professor Appraisal Files'},
        ),
    ]
