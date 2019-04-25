from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'clients'

urlpatterns = [
    path('invite/manager', views.invite_manager, name='invite_manager')
]

router = DefaultRouter()
router.register(r'hire', views.HireInvitationViewSet, 'hire_invitation')
router.register(r'', views.ClientViewSet, 'clients')
urlpatterns = urlpatterns + router.urls
