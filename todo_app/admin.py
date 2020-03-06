from django.contrib import admin
from .models import Task

# custom task field in admin page


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['task_name']}),
        ('Date information', {'fields': [
         'date_created'], 'classes': ['collapse']}),
    ]
    list_display = ('task_name', 'task_desc', 'completed',
                    'date_created', 'image', 'doc', 'owner_id')
    list_filter = ['date_created']
    search_fields = ['task_name']  # search word
    list_per_page = 3  # paging
    date_hierarchy = 'date_created'


# add to admin page
admin.site.register(Task, TaskAdmin)
