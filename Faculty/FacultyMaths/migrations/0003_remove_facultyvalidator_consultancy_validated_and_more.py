# Generated by Django 4.1.6 on 2023-03-21 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyMaths', '0002_alter_mathgoalsheetassistantprofoncontract_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facultyvalidator',
            name='consultancy_validated',
        ),
        migrations.RemoveField(
            model_name='facultyvalidator',
            name='dissertation_validated',
        ),
        migrations.RemoveField(
            model_name='facultyvalidator',
            name='patents_validated',
        ),
    ]
