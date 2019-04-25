from django.contrib import admin

from .models import Manager


class ManagerAdmin(admin.ModelAdmin):
    model = Manager
    list_display = ('user', 'first_name', 'last_name', 'ssn', 'phone', 'status')
    search_fields = ('first_name', 'status')


admin.site.register(Manager, ManagerAdmin)
