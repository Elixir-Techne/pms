from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.clients.models import Client
from apps.employees.models import Employee
from apps.manager.models import Manager
from apps.masters.models import Country, State, City
from core.base_model import Base
from core.constants import PROJECT_STATUS, BILLING_METHOD, USER_STATUS


class Customer(Base):
    client = models.ForeignKey(Client, related_name='customer_client', on_delete=models.CASCADE)
    first_name = models.CharField(_("First Name"), null=False, max_length=250, blank=True)
    last_name = models.CharField(_("Last Name"), null=False, max_length=250, blank=True)
    email = models.EmailField(_('Email Address'), blank=True)
    phone = models.CharField(_("Phone Number"), null=False, max_length=50, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=10, null=True, blank=True)
    status = models.CharField(_("Status"), choices=USER_STATUS, default=USER_STATUS.pending, max_length=25)

    def __str__(self):
        return "{0} ({1})".format(self.first_name, self.client)

    class Meta:
        db_table = "pms_clients_customers"
        verbose_name_plural = "Clients Customers"


class Project(Base):
    name = models.CharField(_('Project Name'), max_length=100)
    manager = models.ForeignKey(Manager, related_name='project_manager', on_delete=models.CASCADE, null=True,
                                blank=True)
    customer = models.ForeignKey(Customer, related_name='project_customer', on_delete=models.CASCADE)
    description = models.TextField(_('Project Description'), null=True, blank=True)
    billing_method = models.CharField(_('Billing Method'), choices=BILLING_METHOD, default=BILLING_METHOD.fixed_cost,
                                      max_length=25)
    status = models.CharField(_('Project Status'), choices=PROJECT_STATUS, default=PROJECT_STATUS.in_progress,
                              max_length=25)
    estimation = models.CharField(_('Effort Estimation'), max_length=20, null=True, blank=True)
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    members = models.ManyToManyField(Employee, through='EmployeeProject', blank=True,
                                     related_name='project_members')

    def __str__(self):
        return "{0} ({1})".format(self.name, self.customer)

    class Meta:
        db_table = "pms_clients_customers_project"
        verbose_name_plural = "Projects"


class EmployeeProject(Base):
    employee = models.ForeignKey(Employee, related_name='project_employee', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='project_user_project', on_delete=models.CASCADE)
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    allocation = models.FloatField(_('Allocated Hours'), default=8.00)

    def __str__(self):
        return "{0}->{1}".format(self.employee, self.project)

    class Meta:
        unique_together = ('employee', 'project')
        db_table = "pms_employees_projects"
        verbose_name_plural = "Employee-Project Allocations"
