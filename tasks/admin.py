from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'created_date', 'due_date']
    list_filter = ['status', 'priority', 'created_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_date'
