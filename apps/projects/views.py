from __future__ import absolute_import

import logging

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.functions import PmsResponse
from core.renderes import PmsJSONRenderer
from .models import Customer, Project, EmployeeProject
from .serializers import CustomerSerializer, ProjectSerializer, EmployeeProjectSerializer

logger = logging.getLogger(__name__)


class CustomerView(viewsets.ModelViewSet):
    model = Customer
    serializer_class = CustomerSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.all()


class ProjectView(viewsets.ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()


class ProjectEmployeeView(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    model = EmployeeProject
    serializer_class = EmployeeProjectSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = EmployeeProject.objects.all()


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_projects(request):
    try:
        user = request.user
        if user.is_superuser:
            logger.info('admin not have permission to access project.')
            return PmsResponse(
                {"msg": "admin not have permission to access project."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info('request to get %s user projects.' % user)
        if Project.objects.filter(manager__user=user.id).exists():
            logger.info('trying to get %s manager projects.' % user)
            projects = Project.objects.filter(manager__user=user.id)
            logger.info('%s manager project getting successfully.' % user)
            return PmsResponse(
                ProjectSerializer(instance=projects, many=True).data,
                status=status.HTTP_200_OK,
            )
        elif EmployeeProject.objects.filter(employee__user=user.id).exists():
            logger.info('trying to get %s employee projects.' % user)
            project_employee = EmployeeProject.objects.get(employee__user=user.id)
            projects = Project.objects.filter(pk=project_employee.project.id)
            logger.info('%s employee project getting successfully.' % user)
            return PmsResponse(
                ProjectSerializer(instance=projects, many=True).data,
                status=status.HTTP_200_OK,
            )
        elif Project.objects.filter(customer__client__user=user.id).exists():
            logger.info('trying to get %s client projects.' % user)
            projects = Project.objects.filter(customer__client__user=user.id)
            logger.info('%s project getting successfully.' % user)
            return PmsResponse(
                ProjectSerializer(instance=projects, many=True).data,
                status=status.HTTP_200_OK,
            )
    except Project.DoesNotExist:
        logger.warning('requested project not exists in system.')
        return PmsResponse(
            {"msg": "Project not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to get %s projects.' % user)
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to get %s projects." % user.username},
            status=status.HTTP_400_BAD_REQUEST,
        )
