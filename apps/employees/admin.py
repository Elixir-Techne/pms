from __future__ import absolute_import

from django.conf import settings
from django.contrib import admin

from .models import Employee, EmploymentCompensation, Bank, Paycheck


class EmployeeProfileAdmin(admin.ModelAdmin):
    model = Employee
    raw_id_fields = ['country', 'state', 'city']
    list_display = ['user', 'ssn', 'phone', 'status']

    if not settings.DEV_DEBUG:
        def get_readonly_fields(self, request, obj=None):
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


class EmploymentCompensationAdmin(admin.ModelAdmin):
    model = EmploymentCompensation
    list_display = ['company', 'location', 'title', 'annual_salary', 'direct_reports', 'is_current']


class BankAdmin(admin.ModelAdmin):
    model = Bank
    list_display = ['type', 'routing_number', 'account_number', 'name', 'address']


class PaycheckAdmin(admin.ModelAdmin):
    model = Paycheck
    list_display = ['method', 'distribution', 'notes']


admin.site.register(Employee, EmployeeProfileAdmin)
admin.site.register(EmploymentCompensation, EmploymentCompensationAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(Paycheck, PaycheckAdmin)
