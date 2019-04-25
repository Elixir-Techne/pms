from rest_framework import mixins, status, viewsets
from rest_framework.decorators import (api_view, detail_route, list_route,
                                       permission_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.functions import PmsResponse
from invitations.app_settings import app_settings as invitations_settings
from invitations.signals import invite_accepted
from .app_settings import (CREATE_AND_SEND_URL, SEND_MULTIPLE_URL, SEND_URL,
                           InvitationBulkWriteSerializer, InvitationModel,
                           InvitationReadSerializer, InvitationWriteSerializer)


class InvitationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = InvitationModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InvitationReadSerializer
        elif self.action == 'send_multiple':
            return InvitationBulkWriteSerializer
        return InvitationWriteSerializer

    def _prepare_and_send(self, invitation, request):
        invitation.inviter = request.user
        invitation.save()
        invitation.send_invitation(request)

    @detail_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=SEND_URL
    )
    def send(self, request, pk=None):
        invitation = self.get_object()
        self._prepare_and_send(invitation, request)
        content = {'msg': 'Invite sent'}
        return Response(content, status=status.HTTP_200_OK)

    @list_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=CREATE_AND_SEND_URL
    )
    def create_and_send(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        type = serializer.data['type']
        invitation = InvitationModel.create(email=email, inviter=request.user, type=type)
        self._prepare_and_send(invitation, request)
        content = {'msg': 'Invite sent'}
        return Response(content, status=status.HTTP_200_OK)

    @list_route(
        methods=['post'], permission_classes=[IsAuthenticated],
        url_path=SEND_MULTIPLE_URL
    )
    def send_multiple(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        inviter = request.user
        error_msg = {}
        content = {}
        is_exists = True
        for email in serializer.data['email']:
            if not InvitationModel.objects.filter(email=email).exists():
                type = serializer.data['type']
                invitation = InvitationModel.create(email=email, inviter=inviter, type=type)
                self._prepare_and_send(invitation, request)
                error_msg[email] = 'Invite sent'
                is_exists = False
            else:
                error_msg[email] = 'invitation with this e-mail address already exists.'
        if not is_exists:
            content.update({'msg': 'Invite(s) sent'})
            status_code = status.HTTP_200_OK
        else:
            status_code = status.HTTP_400_BAD_REQUEST
        content.update(error_msg)
        return Response(content, status=status_code)


@api_view(('POST', 'GET'))
@permission_classes((AllowAny,))
def accept_invitation(request, key):
    def get_object():
        try:
            return InvitationModel.objects.get(key=key.lower())
        except InvitationModel.DoesNotExist:
            return None

    invitation = get_object()

    login_data = {
        'LOGIN_REDIRECT': invitations_settings.LOGIN_REDIRECT
    }
    signup_data = {
        'SIGNUP_REDIRECT': invitations_settings.SIGNUP_REDIRECT
    }

    if invitations_settings.GONE_ON_ACCEPT_ERROR and (not invitation or (invitation and (invitation.key_expired()))):
        login_data = {
            'msg': 'An invalid/expired/previously accepted invitation was submitted.'
        }
        return Response(login_data, status=status.HTTP_400_BAD_REQUEST)

    if not invitation:
        login_data.update({
            'msg': 'An invalid invitation key was submitted.'
        })
        return Response(login_data, status=status.HTTP_400_BAD_REQUEST)

    if invitation.accepted:
        already_accepted = {'msg': 'The invitation for %s was already accepted' % invitation.email}
        return Response(already_accepted, status=status.HTTP_400_BAD_REQUEST)

    if invitation.key_expired():
        signup_data.update({
            'msg': 'The invitation for %s has expired.' % invitation.email
        })
        return Response(signup_data, status=status.HTTP_400_BAD_REQUEST)
    signup_data.update(
        {
            'account_verified_email': invitation.email,
            'msg': 'Invitation to - %s - has been accepted' % invitation.email
        }
    )
    if not invitations_settings.ACCEPT_INVITE_AFTER_SIGNUP:
        invitation.accepted = True
        invitation.save()
        invite_accepted.send(sender=None, email=invitation.email)
    return Response(
        signup_data,
        status=status.HTTP_200_OK
    )


@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def search_invitation(request):
    try:
        invitation_status = request.data['status']
        if invitation_status == 'pending':
            accepted = False
        elif invitation_status == 'approved':
            accepted = True
        else:
            return PmsResponse(
                {"msg": "Invalid search parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        invitation = InvitationModel.objects.filter(accepted=accepted)
        return PmsResponse(
            InvitationReadSerializer(instance=invitation, many=True).data,
            status=status.HTTP_200_OK,
        )
    except InvitationModel.DoesNotExist:
        return PmsResponse(
            {"msg": "Invitation not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        return PmsResponse(
            {"msg": "Failed to search invitation."},
            status=status.HTTP_400_BAD_REQUEST,
        )
