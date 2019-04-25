from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.masters.models import Country, State, City
from core.base_model import Base
from core.constants import USER_GENDER, USER_STATUS


class Manager(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(_("Profile Image"), upload_to='profile/manager', blank=True, null=True)
    gender = models.CharField(_('Employee Gender'), choices=USER_GENDER, default=USER_GENDER.male, max_length=25)
    first_name = models.CharField(_("First Name"), null=True, max_length=250, blank=True)
    last_name = models.CharField(_("Last Name"), null=True, max_length=250, blank=True)
    ssn = models.CharField(_("Employee SSN"), null=False, max_length=50, blank=True)
    birth_date = models.DateField(_("Employee Date of Birth"), null=True, blank=True)
    address_1 = models.CharField(_("Address 1"), max_length=255, null=True, blank=True)
    address_2 = models.CharField(_("Address 2"), max_length=255, null=True, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, null=True,blank=True)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, null=True, blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=10, null=True, blank=True)
    phone = models.CharField(_("Employee Phone Number"), null=False, max_length=50, blank=True)
    status = models.CharField(_('Employee Status'), choices=USER_STATUS, default=USER_STATUS.pending, max_length=25)

    def __str__(self):
        return "{0}".format(self.user.username)

    class Meta:
        db_table = "pms_project_manager"
        verbose_name_plural = "Project Manager"
