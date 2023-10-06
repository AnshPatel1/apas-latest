from django.contrib import admin

from MasterConfiguration.models import *


# Register your models here.

class StaffAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class SOTFacultyAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class SPMFacultyAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class SLSFacultyAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class MathFacultyAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class ScienceFacultyAppraisalCycleInclusionAdmin(admin.ModelAdmin):
    filter_horizontal = ('appraisee',)
    search_fields = ('year',)


class RO1ListAdmin(admin.ModelAdmin):
    filter_horizontal = ('ro1_users',)


class RO2ListAdmin(admin.ModelAdmin):
    filter_horizontal = ('ro2_users',)


admin.site.register(StaffAppraisalCycleInclusion, StaffAppraisalCycleInclusionAdmin)
admin.site.register(SOTFacultyAppraisalCycleInclusion, SOTFacultyAppraisalCycleInclusionAdmin)
admin.site.register(SPMFacultyAppraisalCycleInclusion, SPMFacultyAppraisalCycleInclusionAdmin)
admin.site.register(SLSFacultyAppraisalCycleInclusion, SLSFacultyAppraisalCycleInclusionAdmin)
admin.site.register(MathFacultyAppraisalCycleInclusion, MathFacultyAppraisalCycleInclusionAdmin)
admin.site.register(ScienceFacultyAppraisalCycleInclusion, ScienceFacultyAppraisalCycleInclusionAdmin)
admin.site.register(RO1List, RO1ListAdmin)
admin.site.register(RO2List, RO2ListAdmin)
admin.site.register(StaffAppraisalCycleConfiguration)
admin.site.register(FOETFacultyAppraisalCycleConfiguration)
admin.site.register(SLSFacultyAppraisalCycleConfiguration)
admin.site.register(SOEMFacultyAppraisalCycleConfiguration)
admin.site.register(MathFacultyAppraisalCycleConfiguration)
admin.site.register(ScienceFacultyAppraisalCycleConfiguration)
admin.site.register(CurrentDate)
admin.site.register(ShowResult)
