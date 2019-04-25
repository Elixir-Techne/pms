from django.contrib import admin

# Register your models here.
from .models import Contract, ContractDocument


class ContractAdmin(admin.ModelAdmin):
    model = Contract
    list_display = ('employee', 'client', 'start_date', 'end_date', 'payment_mode', 'status')


class ContractDocumentAdmin(admin.ModelAdmin):
    model = ContractDocument
    list_display = ('contract', 'title', 'description', 'created', 'image')


admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractDocument, ContractDocumentAdmin)
