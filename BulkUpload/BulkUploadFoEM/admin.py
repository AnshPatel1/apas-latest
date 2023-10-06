from django.contrib import admin

# Register your models here.
from .models import *


class UploadCSVAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_type', 'file')
    list_filter = ('upload_type',)
    search_fields = ('upload_type',)
    actions = ['delete_selected']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class VerifyUploadedAdmin(admin.ModelAdmin):
    list_display = ('csv_origin', 'is_verified')
    list_filter = ('csv_origin__upload_type', 'is_verified')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewAcademiaCollaborationAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'mou_marks', 'marks')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewCoCurricularAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'marks')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewPatentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'status', 'description', 'month', 'year', 'application_no')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'status', 'month', 'year', 'application_no')
    list_filter = ('faculty', 'designation', 'department', 'status', 'month', 'year')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewConsultancyAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'type', 'description', 'amount', 'month', 'year')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'type', 'month', 'year')
    list_filter = ('designation', 'department', 'type', 'month', 'year')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewAwardAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'title', 'description', 'level', 'month', 'year')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'title', 'description')
    list_filter = ('designation', 'department', 'level', 'month', 'year')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewPhDGuidanceAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'status', 'student_name', 'year')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'status', 'student_name', 'year')
    list_filter = ('faculty', 'designation', 'department', 'status', 'year')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewProjectAdmin(admin.ModelAdmin):
    list_display = (
        'faculty', 'designation', 'department', 'title', 'status', 'funding_agency', 'amount', 'role', 'year', 'month', 'is_institutional', 'is_osrp', 'institutional_marks')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'title', 'status', 'funding_agency', 'amount')
    list_filter = ('faculty', 'designation', 'department', 'status', 'role', 'year', 'month', 'is_institutional', 'is_osrp')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewScopusWosAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'month', 'year', 'type', 'title', 'entity_name', 'paper_quality', 'isbn', 'conference_organization', 'conference_level',
                    'is_main_author', 'co_author_count', 'is_scopus', 'is_wos', 'is_ugc', 'is_abdc')
    search_fields = (
        'faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'title', 'entity_name', 'paper_quality', 'isbn', 'conference_organization')
    list_filter = ('faculty', 'designation', 'department', 'month', 'year', 'type', 'conference_level',
                   'is_main_author', 'co_author_count', 'is_scopus', 'is_wos', 'is_ugc', 'is_abdc')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewBookAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'month', 'year', 'level', 'title', 'category', 'type', 'is_main_author', 'co_author_count', 'is_editor', 'isbn')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department', 'title', 'isbn')
    list_filter = ('faculty', 'designation', 'department', 'month', 'year', 'level', 'category', 'type', 'is_main_author', 'co_author_count', 'is_editor')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewExamDutyAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'timely_invigilation', 'paper_setting', 'evaluation', 'result_submission')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewStudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'student_feedback')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewTeachingLoadAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'load_odd', 'load_even', 'load_tri')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ViewAdditionalMarksAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'designation', 'department', 'placement_activity', 'admission_activity', 'pgp_chair', 'e_mba_chair')
    search_fields = ('faculty__username', 'faculty__first_name', 'faculty__last_name', 'designation', 'department')
    list_filter = ('faculty', 'designation', 'department')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ('upload_type', 'error', 'type', 'created_at', 'created_by')
    list_filter = ('upload_type', 'type', 'created_by')

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


admin.site.register(UploadCSV, UploadCSVAdmin)
admin.site.register(Template)
admin.site.register(VerifyUploaded, VerifyUploadedAdmin)
admin.site.register(ViewAcademiaCollaboration, ViewAcademiaCollaborationAdmin)
admin.site.register(ViewCoCurricular, ViewCoCurricularAdmin)
admin.site.register(ViewConsultancy, ViewConsultancyAdmin)
admin.site.register(ViewAward, ViewAwardAdmin)
admin.site.register(ViewPhDGuidance, ViewPhDGuidanceAdmin)
admin.site.register(ViewProject, ViewProjectAdmin)
admin.site.register(ViewScopusWos, ViewScopusWosAdmin)
admin.site.register(ViewBook, ViewBookAdmin)
admin.site.register(ViewExamDuty, ViewExamDutyAdmin)
admin.site.register(ViewStudentFeedback, ViewStudentFeedbackAdmin)
admin.site.register(ViewTeachingLoad, ViewTeachingLoadAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)
admin.site.register(ViewAdditionalMarks, ViewAdditionalMarksAdmin)
