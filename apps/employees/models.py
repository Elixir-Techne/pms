from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.masters.models import (Country, State, City)
from core.base_model import Base
from core.constants import (USER_STATUS, USER_GENDER, COMPENSATION_TYPE, EMPLOYMENT_TYPE, ACCOUNT_TYPE, PAYCHECK_METHOD,
                            EMPLOYMENT_AVAILABILITY)


# Create your models here.

class Employee(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(_("Profile Image"), upload_to='profile/employees', blank=True, null=True)
    gender = models.CharField(_('Employee Gender'), choices=USER_GENDER, default=USER_GENDER.male, max_length=25)
    first_name = models.CharField(_("First Name"), null=False, max_length=250, blank=True)
    last_name = models.CharField(_("Last Name"), null=False, max_length=250, blank=True)
    ssn = models.CharField(_("Employee SSN"), null=False, max_length=50, blank=True)
    birth_date = models.DateField(_("Employee Date of Birth"), null=True, blank=True)
    address_1 = models.CharField(_("Address 1"), max_length=255)
    address_2 = models.CharField(_("Address 2"), max_length=255, null=True, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=10, null=True, blank=True)
    phone = models.CharField(_("Employee Phone Number"), null=False, max_length=50, blank=True)
    status = models.CharField(_('Employee Status'), choices=USER_STATUS, default=USER_STATUS.pending, max_length=25)
    availability = models.CharField(_('Employee Availability'), choices=EMPLOYMENT_AVAILABILITY,
                                    default=EMPLOYMENT_AVAILABILITY.available, max_length=20)

    def __str__(self):
        return "{0}".format(self.user.username)

    class Meta:
        db_table = "pms_users_employee_profile"
        verbose_name_plural = "Employees"


class EmploymentCompensation(Base):
    employee = models.ForeignKey(Employee, related_name="compensations",
                                 on_delete=models.CASCADE)
    company = models.CharField(_("Company"), null=True, max_length=250, blank=True)
    location = models.CharField(_("Location"), null=True, max_length=250, blank=True)
    title = models.CharField(_("Title"), null=True, max_length=250, blank=True)
    start_date = models.DateField(_("Start Date"), null=True)
    end_date = models.DateField(_("End Date"), null=True)
    department = models.CharField(_("Department"), max_length=100, null=True, blank=True)
    compensation_type = models.CharField(_('Compensation Type'), choices=COMPENSATION_TYPE,
                                         default=COMPENSATION_TYPE.salaried, max_length=25)
    employment_type = models.CharField(_('Employment Type'), choices=EMPLOYMENT_TYPE,
                                       default=EMPLOYMENT_TYPE.full_time, max_length=25)
    annual_salary = models.IntegerField(_("Annual Salary"), default=0)
    job_duties = models.CharField(_("Performs Exempt Job Duties"), max_length=250, blank=True)
    flsa_classification = models.CharField(_("FLSA Classification"), max_length=250, blank=True)
    manager = models.CharField(_("Manager"), max_length=250, blank=True)
    direct_reports = models.CharField(_("Direct Reports"), max_length=250, blank=True)
    is_current = models.BooleanField(_("Is Current?"), default=False)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.title)

    class Meta:
        db_table = "pms_employee_employments_compensations"
        verbose_name_plural = "Employee Employments And Compensations"


class Bank(Base):
    employee = models.ForeignKey(Employee, related_name="bank",
                                 on_delete=models.CASCADE)
    type = models.CharField(_('Account Type'), choices=ACCOUNT_TYPE,
                            default=ACCOUNT_TYPE.saving, max_length=25)
    routing_number = models.CharField(_('Routing Number'), max_length=100, blank=True)
    account_number = models.CharField(_('Account Number'), max_length=100, blank=True)
    name = models.CharField(_('Name'), max_length=100, blank=True)
    address = models.CharField(_('Address'), max_length=100, blank=True)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    def __str__(self):
        return "{0}".format(self.type)

    class Meta:
        db_table = "pms_employee_banks"
        verbose_name_plural = "Employee Bank Information"


class Paycheck(Base):
    employee = models.ForeignKey(Employee, related_name="paycheck",
                                 on_delete=models.CASCADE)
    method = models.CharField(_('Method'), choices=PAYCHECK_METHOD, default=PAYCHECK_METHOD.bank, max_length=25)
    distribution = models.CharField(_('Distribution'), max_length=250, blank=True)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    def __str__(self):
        return "0".format(self.method)

    class Meta:
        db_table = "pms_employee_paycheck"
        verbose_name_plural = "Employee Paychecks"
