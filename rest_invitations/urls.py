from django.conf.urls import include, url
from django.urls import path
from rest_framework import routers

from .app_settings import ACCEPT_INVITE_URL, API_BASE_URL
from .views import InvitationViewSet, accept_invitation, search_invitation

router = routers.SimpleRouter()
router.register(r'api/v1/users/{0}'.format(API_BASE_URL), InvitationViewSet)

invitations_patterns = (
    [
        url(
            r'^api/v1/users/{0}/{1}/(?P<key>\w+)/?$'.format(
                API_BASE_URL, ACCEPT_INVITE_URL
            ),
            accept_invitation,
            name='accept-email'
        ),
        url(
            r'^pages/register/(?P<key>\w+)/?$',
            accept_invitation,
            name='accept-invite'
        ),

    ],
    'invitations'
)

urlpatterns = router.urls + [
    url(r'^', include(invitations_patterns)),
    path('api/v1/users/invitations/search', search_invitation, name='search_invitation'),
]
