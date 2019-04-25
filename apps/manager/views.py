from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.functions import PmsResponse
from core.renderes import PmsJSONRenderer
from .models import Manager
from .serializers import ManagerSerializer


class ManagerView( mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    model = Manager
    serializer_class = ManagerSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Manager.objects.all()



