from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=100)
    short_name = models.CharField(_("Country Short Name"), max_length=3)
    iso_3 = models.CharField(_("Country ISO3 Name"), max_length=5, blank=True, null=True)
    phone_code = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "pms_masters_countries"
        verbose_name_plural = _("Manage Countries")
        ordering = ('name',)


class State(models.Model):
    name = models.CharField(_("State Name"), max_length=100)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "pms_masters_states"
        verbose_name_plural = _("Manage States")
        ordering = ('name',)


class City(models.Model):
    name = models.CharField(_("City Name"), max_length=100)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = "pms_masters_cities"
        verbose_name_plural = _("Manage Cities")
        ordering = ('name',)
