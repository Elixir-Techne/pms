from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import (Country, State, City)


class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "iso_3")
    model = Country
    search_fields = ['name', 'phone_code']
    ordering = ('name',)


class StateAdmin(admin.ModelAdmin):
    list_display = ("country", "name")
    model = State
    list_filter = ("country",)
    search_fields = ['name', 'country__name']
    ordering = ('country__name', 'name')


class CityAdmin(admin.ModelAdmin):
    list_display = ("state", "name")
    model = City
    list_filter = ("state",)
    search_fields = ['name', 'state__name']
    ordering = ('state__name', 'name')


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
