import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.contracts.models import Contract
from apps.employees.models import Employee
from apps.manager.models import Manager
from apps.projects.models import Customer, Project
from core.functions import PmsResponse
from pms import settings
from .models import Client, HireInvitation
from .permissions import ClientPermission
from .serializers import ClientSerializer, HireInvitationSerializer

logger = logging.getLogger(__name__)


class ClientViewSet(viewsets.ModelViewSet):
    """
    This endpoint presents the clients in the system.
    """
    model = Client
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (ClientPermission,)


def send_email(msg_html, template_email_text, from_email, recipient_list, subject):
    logger.info('%s mail send successfully.' % str(recipient_list))
    return send_mail(subject, template_email_text, from_email,
                     recipient_list, html_message=msg_html, fail_silently=False)


class HireInvitationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    model = HireInvitation
    queryset = HireInvitation.objects.all()
    serializer_class = HireInvitationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            logger.info('trying to send hire invitation to employee.')
            inviter = request.user
            employee = Employee.objects.get(pk=request.data['employee'])
            if HireInvitation.objects.filter(employee=employee, inviter=inviter, accepted=False).exists():
                logger.warning('hire invitation email already sent to %s' % employee.user)
                return PmsResponse(
                    {"msg": "The invitation email already sent."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            to_email = employee.user.email
            key = get_random_string(64).lower()
            HireInvitation.objects.create(inviter=inviter, employee=employee, key=key)
            invite_url = reverse('clients:hire_invitation-detail',
                                 args=[key])
            invite_url = settings.FRONT_END_SERVER + invite_url
            data = {
                'email': to_email,
                'client': inviter,
                'invite_url': invite_url
            }
            from_mail = 'webmaster@localhost'
            if hasattr(settings, 'DEFAULT_FROM_EMAIL'):
                from_mail = settings.DEFAULT_FROM_EMAIL
            msg_html = render_to_string('hire/email/email_invite_message.txt', data)
            logger.info('trying to send hire invitation email to %s.' % to_email)
            send_mail(subject='Invitation to join', message=msg_html, from_email=from_mail,
                      recipient_list=(to_email,))
            logger.info('%s email sent successfully.' % to_email)
            return PmsResponse(
                {"msg": "Hire Invitation email send to %s successfully." % to_email},
                status=status.HTTP_200_OK,
            )
        except Employee.DoesNotExist:
            logger.warning('%s employee not exists in system.' % request.data['employee'])
            return PmsResponse(
                {"msg": "Employee not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as ex:
            logger.error('failed to send hire invitation email to %s.' % to_email)
            return PmsResponse(
                {"msg": "Failed to send invitation to %s." % to_email},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            logger.info('hire invitation conformation request...')
            key = kwargs['pk']
            if not HireInvitation.objects.filter(key=key).exists():
                logger.error('invalid hire invitation key was submitted.')
                return PmsResponse(
                    {"msg": "An invalid hire invitation key was submitted."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            hire_invitation = HireInvitation.objects.get(key=key)
            if hire_invitation.accepted:
                logger.warning('hire invitation for %s was already accepted.' % hire_invitation.employee.user.email)
                return PmsResponse(
                    {"msg": "The invitation for - %s - was already accepted." % hire_invitation.employee.user.email},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            hire_invitation.accepted = True
            hire_invitation.save()
            client = Client.objects.get(user=hire_invitation.inviter)
            Contract.objects.create(employee=hire_invitation.employee, client=client)
            logger.info('hire invitation has been accepted for %s.' % hire_invitation.employee.user.email)
            return PmsResponse(
                {"msg": "Hire invitation to - %s - has been accepted." % hire_invitation.employee.user.email},
                status=status.HTTP_200_OK,
            )
        except Client.DoesNotExist:
            logger.error('client not exists in system.')
            return PmsResponse(
                {"msg": "Client not exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as ex:
            logger.error('failed to add contract.')
            logger.exception(ex)
            return PmsResponse(
                {"msg": "Failed to add contract."},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def invite_manager(request):
    try:
        logger.info('request for invite project manager by client.')
        email = request.data['email']
        validate_email(email)
        logger.info('trying to create user account for %s manager.' % email)
        if not User.objects.filter(email=email).exists():
            client = Client.objects.get(user=request.user)
            customer = Customer.objects.get(client=client)
            project = Project.objects.get(customer=customer)
            user = User()
            user.username = email
            user.email = email
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            manager = Manager.objects.create(user=user)
            project.manager = manager
            project.save()
            logger.info('account created successfully for %s.' % email)
            data = {
                'email': email,
                'password': password,
            }
            from_mail = 'webmaster@localhost'
            if hasattr(settings, 'DEFAULT_FROM_EMAIL'):
                from_mail = settings.DEFAULT_FROM_EMAIL
            msg_html = render_to_string('hire/email/manager_email_invite_message.txt', data)
            logger.info('trying to send login information on %s email.' % email)
            send_mail(subject='Invitation to join as manager', message=msg_html, from_email=from_mail,
                      recipient_list=(email,))
            logger.info('email sent successfully to %s for project manager.' % email)
            return PmsResponse(
                {"msg": "Manager invitation send to %s successfully." % email},
                status=status.HTTP_200_OK,
            )
        else:
            logger.error('%s email already exists in system.' % email)
            return PmsResponse(
                {'msg': '%s email already exists in system.' % email},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except ValidationError as e:
        logger.error('%s is invalid email.' % email)
        logger.error(e)
        return PmsResponse(
            {'msg': 'oops! invalid email'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to invite manager.')
        logger.exception(ex)
        return PmsResponse(
            {'msg': 'Failed to invite manager.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
