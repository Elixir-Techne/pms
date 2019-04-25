from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.employees.models import Employee
from apps.projects.models import Project
from core.base_model import Base
from core.constants import BILLING_METHOD, TASK_STATUS


# Create your models here.
class TaskCategory(Base):
    name = models.CharField(_("Task Category"), max_length=255, unique=True)
    description = models.TextField(default='', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "pms_tasks_category"
        verbose_name_plural = "Task Categories"


class Task(Base):
    project = models.ForeignKey(Project, related_name="task_project", on_delete=models.CASCADE)
    title = models.CharField(_("Task Title"), max_length=255)
    category = models.ForeignKey(TaskCategory, related_name="task_category", on_delete=models.CASCADE)
    description = models.TextField(_("Task Description"), default='', null=True)
    creator = models.ForeignKey(Employee, related_name="task_creator", on_delete=models.CASCADE)
    assign = models.ForeignKey(Employee, related_name="task_assign", on_delete=models.CASCADE)
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    billing_method = models.CharField(_('Billing Method'), choices=BILLING_METHOD, default=BILLING_METHOD.fixed_cost,
                                      max_length=25)
    status = models.CharField(_('Project Status'), choices=TASK_STATUS, default=TASK_STATUS.in_progress, max_length=25)
    effort = models.DecimalField(_("Estimated Hours"), max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return "{0} ({1})".format(self.title, self.project.name)

    class Meta:
        db_table = "pms_tasks_task"
        verbose_name_plural = "Project Tasks"
