import datetime

from django.core.files import File
from django.db import models
from django.contrib.admin.models import LogEntry
from django.utils.safestring import mark_safe
from pandas import DataFrame
from APAS import settings
import os


# Create your models here.

class CreateLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    log_file = models.FileField(upload_to='logs/', editable=False)
    generated_name = models.CharField(max_length=1000, editable=False)

    # download_link = models.CharField(max_length=1000, editable=False)

    def __str__(self):
        return 'Created at ' + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def clean(self):
        logs = LogEntry.objects.all()
        log_list = []
        action_flag = {
            1: 'Add',
            2: 'Change',
            3: 'Deletion',
        }
        for l in logs:
            temp = {'user': l.user, 'action_time': l.action_time.strftime("%m/%d/%Y, %H:%M:%S"), 'action': action_flag[l.action_flag], 'details': l.object_repr}
            log_list.append(temp)
        df = DataFrame(log_list)
        time = datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        df.to_excel(f'media/logs/generated/{time}.xlsx', index=False)
        name = f'{time}.xlsx'
        self.generated_name = name
        with open(f'media/logs/generated/{time}.xlsx', 'rb') as f:
            self.log_file.save(name, File(f))

    def delete(self, using=None, keep_parents=False):
        os.remove(self.log_file.path)
        os.remove(os.path.join(settings.MEDIA_ROOT, 'logs/generated', self.generated_name))
        super().delete()
