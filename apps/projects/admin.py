from __future__ import absolute_import

from django.contrib import admin

from .models import Customer, Project, EmployeeProject


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('client', 'first_name', 'last_name', 'email', 'phone', 'status')

    search_fields = ('first_name', 'status')


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', 'description', 'manager', 'customer', 'billing_method', 'estimation', 'start_date',
                    'end_date', 'status')
    search_fields = ('name', 'status')


class EmployeeProjectAdmin(admin.ModelAdmin):
    model = EmployeeProject
    list_display = ('employee', 'project', 'start_date', 'end_date', 'allocation')


admin.site.register(EmployeeProject, EmployeeProjectAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)
