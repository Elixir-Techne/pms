from __future__ import absolute_import

from django.contrib import admin

# Register your models here.
from .models import Client, HireInvitation


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('name', 'email', 'user', 'phone')
    exclude = ('created_date', 'updated_date')


class HireInvitationAdmin(admin.ModelAdmin):
    model = HireInvitation
    list_display = ('employee', 'inviter', 'accepted')


admin.site.register(Client, ClientAdmin)
admin.site.register(HireInvitation, HireInvitationAdmin)
