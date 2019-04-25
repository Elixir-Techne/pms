from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

BILLING_METHOD = Choices(
    ('fixed_cost', _('Fixed Cost')),
    ('method_2', _('Method Two'))
)
PROJECT_STATUS = Choices(
    ('in_progress', _('In Progress')),
    ('completed', _('Completed'))
)
TASK_STATUS = Choices(
    ('in_progress', _('In Progress')),
    ('completed', _('Completed'))
)

USER_STATUS = Choices(
    ('pending', _('Pending')),
    ('approved', _('Approved')),
    ('blocked', _('Blocked'))
)

USER_TYPE = Choices(
    ('admin', _('Admin')),
    ('client', _('Client')),
    ('employee', _('Employee'))
)

USER_GENDER = Choices(
    ('male', _('Male')),
    ('female', _('Female')),
    ('transgender', _('Transgender')),
)

DOCUMENT_STATUS = Choices(
    (1, 'no_document', _('No Document')),
    (2, 'uploaded', _('Uploaded')),
    (3, 'verified', _('Verified')),
)

COMPENSATION_TYPE = Choices(
    ('salaried', _('Salaried')),
    ('daily_payout', _('Daily Payout')),
    ('fixed_payout', _('Fixed payout')),
)

PAYMENT_MODE = Choices(
    ('fixed', _('Fixed')),
    ('hourly', _('Hourly')),
)

CONTRACT_STATUS = Choices(
    ('in_progress', _('In Progress')),
    ('completed', _('Completed'))
)

EMPLOYMENT_TYPE = Choices(
    ('full_time', _('Full Time')),
    ('part_time', _('Part Time')),
    ('contract', _('Contract')),
)

EMPLOYMENT_AVAILABILITY = Choices(
    ('available', _('Available')),
    ('not_available', _('Not Available')),
    ('hired', _('Hired')),
)

ACCOUNT_TYPE = Choices(
    ('saving', _('Saving')),
    ('current', _('Current')),
)

PAYCHECK_METHOD = Choices(
    ('bank', _('Bank')),
    ('paypal', _('Paypal')),
)
