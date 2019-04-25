from django.contrib import admin

from .models import Task, TaskCategory


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('project', 'title', 'category', 'creator', 'assign', 'start_date', 'end_date', 'effort')
    search_fields = ('title', 'status')


class TaskCategoryAdmin(admin.ModelAdmin):
    model = TaskCategory
    list_display = ('name', 'description')
    search_fields = ('name',)


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)
