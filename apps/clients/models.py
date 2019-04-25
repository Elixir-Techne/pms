from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.employees.models import Employee
from core.base_model import Base
# Create your models here.
from core.constants import USER_STATUS


class Client(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("Client Name"), max_length=100)
    trade = models.CharField(_("Trade"), max_length=100)
    description = models.CharField(_("Description"), max_length=100)
    email = models.EmailField(_('Email Address'), blank=True)
    address = models.TextField(_("Address"), blank=True, null=True)
    contact_first_name = models.CharField(_('First Name'), max_length=30, blank=True, null=True)
    contact_last_name = models.CharField(_('Last Name'), max_length=30, blank=True, null=True)
    phone = models.CharField(_('Phone Number'), max_length=30, blank=True, null=True)
    status = models.CharField(_('Employee Status'), choices=USER_STATUS, default=USER_STATUS.pending, max_length=25)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.user)

    class Meta:
        db_table = "pms_clients_client"
        verbose_name_plural = "Clients"


class HireInvitation(Base):
    employee = models.ForeignKey(Employee, related_name="hire_employee",
                                 on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name=_('accepted'), default=False)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    inviter = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Hire: {0}".format(self.employee)

    class Meta:
        db_table = "pms_hire_employee"
        verbose_name_plural = "Hire Employee"
