from django.contrib import admin
from .models import CreateLog


# Register your models here.


class CreateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'log_file')
    list_filter = ('created_at',)
    search_fields = ('name', 'created_at')
    fieldsets = (
        (None, {
            'fields': (),
            'description': "Just press save to create a log file. Save button is located at the bottom-right of the page."
        }),
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


admin.site.register(CreateLog, CreateLogAdmin)
