from django.contrib import admin
from .models import *


# Register your models here.


class StaffAppraisalFileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_all_parameters_approved','file_level', 'year']
    list_filter = ['user', 'year', 'file_level']
    search_fields = ['user__username','user__email','user__full_name', 'year']
    filter_horizontal = ['key_parameter', 'major_parameter', 'minor_parameter', 'self_development_parameter', 'cancelled_parameters']

    list_per_page = 25


admin.site.register(File)
admin.site.register(StaffConfiguration)
admin.site.register(StaffAppraisalFile, StaffAppraisalFileAdmin)
admin.site.register(Parameter)
admin.site.register(MarkField)
admin.site.register(Certificate)
admin.site.register(StaffValidation)
admin.site.register(GradeConfiguration)
