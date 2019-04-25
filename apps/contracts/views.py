import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.constants import CONTRACT_STATUS
from core.functions import PmsResponse
from .models import Contract, ContractDocument
from .serializers import ContractSerializer, ContractDocumentSerializer

logger = logging.getLogger(__name__)


class ContractViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    model = Contract
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)


class ContractDocumentViewSet(viewsets.ModelViewSet):
    model = ContractDocument
    queryset = ContractDocument.objects.all()
    serializer_class = ContractDocumentSerializer
    permission_classes = (IsAuthenticated,)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_contract(request):
    try:
        logger.info('trying to get %s employee documents.' % request.user)
        user = request.user
        contracts = Contract.objects.filter(employee__user=user.id, status=CONTRACT_STATUS.in_progress)
        return PmsResponse(
            ContractSerializer(instance=contracts, many=True).data,
            status=status.HTTP_200_OK,
        )
    except Contract.DoesNotExist:
        logger.warning('%s employee contract not exists.' % request.user)
        return PmsResponse(
            {"msg": "Contract not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to get %s employee contract.' % request.user)
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to get employee documents."},
            status=status.HTTP_400_BAD_REQUEST,
        )
