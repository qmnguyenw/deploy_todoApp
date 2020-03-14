from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['task_name', 'task_desc', 'completed',
                                         'image', 'doc']}),
        # ('Date information', {'fields': [
        #  'date_created'], 'classes': ['collapse']}),
    ]
    list_display = ('task_name', 'task_desc', 'completed',
                    'date_created', 'image', 'doc', 'owner_id')
    list_filter = ['date_created']
    search_fields = ['task_name']
    list_per_page = 3
    # date_hierarchy = 'date_created'

# add to admin page
admin.site.register(Task, TaskAdmin)
