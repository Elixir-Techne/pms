import logging

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.projects.serializers import ProjectSerializer
from core.constants import TASK_STATUS
from core.functions import PmsResponse
from core.renderes import PmsJSONRenderer
from .models import Task, TaskCategory
from .serializers import TaskSerializer, CategorySerializer

logger = logging.getLogger(__name__)


class TaskView(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    model = Task
    serializer_class = TaskSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()


class CategoryView(viewsets.ModelViewSet):
    model = TaskCategory
    serializer_class = CategorySerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = TaskCategory.objects.all()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_project_tasks(request):
    try:
        logger.info('trying to get %s employee project tasks.' % request.user)
        user = request.user
        tasks = Task.objects.filter(assign__user=user, status=TASK_STATUS.in_progress)
        projects = [task.project for task in tasks]
        projects = list(set(projects))
        return PmsResponse(
            ProjectSerializer(instance=projects, many=True).data,
            status=status.HTTP_200_OK,
        )
    except Task.DoesNotExist:
        logger.warning('%s employee project tasks not exists.' % request.user)
        return PmsResponse(
            {"msg": "Contract not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to get %s employee project tasks.' % request.user)
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to get employee project tasks."},
            status=status.HTTP_400_BAD_REQUEST,
        )
