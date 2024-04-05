import os

from django.db import models
from pandas import DataFrame
from django.core.files import File as DjangoFile
from APAS import settings
from Staff.models import *
from MasterConfiguration.models import *


# Create your models here.

class StaffParameters(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    log_file = models.FileField(upload_to='reports/', null=True, blank=True)
    # download_link = models.CharField(max_length=1000, editable=False)

    def __str__(self):
        return 'Created at ' + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Staff Parameter Report'
        verbose_name_plural = 'Staff Parameter Reports'

    def clean(self):
        appraisees = StaffAppraisalCycleInclusion.objects.first().appraisee.all()
        files = StaffAppraisalFile.objects.filter(user__in=appraisees)
        print(files)
        data = []
        for file in files:
            d = {
                "username": file.user.username,
                "name": file.user.full_name,
                "email": file.user.email,
                "department": file.user.department,
                "key_1": "",
                "key_detail1": "",
                "key_2": "",
                "key_detail2": "",
                "key_3": "",
                "key_detail3": "",
                "key_4": "",
                "key_detail4": "",
                "key_5": "",
                "key_detail5": "",
                "maj_1": "",
                "maj_detail1": "",
                "maj_2": "",
                "maj_detail2": "",
                "maj_3": "",
                "maj_detail3": "",
                "min_1": "",
                "min_detail1": "",
                "min_2": "",
                "min_detail2": "",
            }
            context = {
                'key_parameter_count': file.key_parameter_count,
                'major_parameter_count': file.major_parameter_count,
                'minor_parameter_count': file.minor_parameter_count,
                'key_parameters': [],
                'major_parameters': [],
                'minor_parameters': []
            }
            for i in range(file.key_parameter_count):
                context['key_parameters'].append(file.key_parameter.all()[i])
            for i in range(file.major_parameter_count):
                context['major_parameters'].append(file.major_parameter.all()[i])
            for i in range(file.minor_parameter_count):
                context['minor_parameters'].append(file.minor_parameter.all()[i])
            for i in range(file.key_parameter_count):
                d[f'key_{i + 1}'] = context['key_parameters'][i].name
                d[f'key_detail{i + 1}'] = context['key_parameters'][i].value
            for i in range(file.major_parameter_count):
                d[f'maj_{i + 1}'] = context['major_parameters'][i].name
                d[f'maj_detail{i + 1}'] = context['major_parameters'][i].value
            for i in range(file.minor_parameter_count):
                d[f'min_{i + 1}'] = context['minor_parameters'][i].name
                d[f'min_detail{i + 1}'] = context['minor_parameters'][i].value
            data.append(d)
            print(d)

        df = DataFrame(data)
        time = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        df.to_excel(f'media/reports/staff/{time}.xlsx')
        name = f'{time}.xlsx'
        self.generated_name = name
        with open(f'media/reports/staff/{name}', 'rb') as f:
            self.log_file.save(name, DjangoFile(f))

    def delete(self, using=None, keep_parents=False):
        os.remove(self.log_file.path)
        os.remove(os.path.join(settings.MEDIA_ROOT, 'reports/staff', self.generated_name))
        super().delete()
