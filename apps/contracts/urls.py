from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'contracts'

urlpatterns = [
    path('my-contracts', views.get_my_contract, name='my_contracts')
]

router = DefaultRouter()
router.register(r'documents', views.ContractDocumentViewSet, 'documents')
router.register(r'', views.ContractViewSet, 'contracts')
urlpatterns = urlpatterns + router.urls
