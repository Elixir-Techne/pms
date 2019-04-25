from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from apps.clients.models import Client
from apps.employees.models import Employee
from core.constants import PAYMENT_MODE, CONTRACT_STATUS


class Contract(models.Model):
    employee = models.ForeignKey(Employee, related_name="contract_employee",
                                 on_delete=models.CASCADE, verbose_name=_('Employee'))
    client = models.ForeignKey(Client, related_name="contract_client",
                               on_delete=models.CASCADE, verbose_name=_('Client'))
    description = models.TextField(_('Description'), blank=True, null=True)
    payment_mode = models.CharField(_('Payment Mode'), choices=PAYMENT_MODE, default=PAYMENT_MODE.fixed,
                                    max_length=25)
    start_date = models.DateTimeField(_("Start Date"), auto_now_add=True)
    end_date = models.DateTimeField(_("End Date"), null=True)
    status = models.CharField(_('Project Status'), choices=CONTRACT_STATUS, default=CONTRACT_STATUS.in_progress,
                              max_length=25)

    def __str__(self):
        return "{0}".format(self.client)

    class Meta:
        db_table = "pms_contract"
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')


class ContractDocument(models.Model):
    contract = models.ForeignKey(Contract, related_name="contract_document",
                                 on_delete=models.CASCADE, verbose_name=_('Contract'))
    title = models.CharField(_('Document title'), max_length=30)
    description = models.TextField(_('Document description'), blank=True, null=True)
    created = models.DateTimeField(_("Created Date"), auto_now_add=True)
    image = models.FileField(_('Document'), null=True, blank=True, upload_to='documents/%Y/%m/%d')

    class Meta:
        db_table = "pms_contract_document"
        verbose_name = _('Contract Document')
        verbose_name_plural = _('Contract Documents')
        ordering = ('title',)
