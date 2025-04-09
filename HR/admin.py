from django.contrib import admin
from HR.models import PatentRecords, PaperRecords, BookRecords

# Register your models here.


admin.site.register(PatentRecords)
admin.site.register(PaperRecords)
admin.site.register(BookRecords)
