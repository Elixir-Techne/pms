import logging

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.constants import EMPLOYMENT_AVAILABILITY
from core.functions import PmsResponse
from core.renderes import PmsJSONRenderer
from .models import Employee, EmploymentCompensation, Bank, Paycheck
from .permissions import EmployeePermission
from .serializers import (EmployeeProfileSerializer, EmploymentCompensationSerializer, BankSerializer,
                          PaycheckSerializer, EmployeeDetailsSerializer)

# Create your views here.
logger = logging.getLogger(__name__)


class EmployeeProfileView(viewsets.ModelViewSet):
    model = Employee
    serializer_class = EmployeeProfileSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated, EmployeePermission)
    queryset = Employee.objects.all()

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_superuser:
                queryset = Employee.objects.all()
            else:
                queryset = Employee.objects.none()
            return queryset
        return Employee.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk')
            employee = Employee.objects.get(pk=id)
            return Response(
                self.serializer_class(employee).data,
                status=status.HTTP_200_OK
            )
        except Employee.DoesNotExist:
            return Response(
                {},
                status=status.HTTP_200_OK
            )


class EmploymentCompensationView(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 GenericViewSet):
    model = EmploymentCompensation
    serializer_class = EmploymentCompensationSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = EmploymentCompensation.objects.all()


class BankView(viewsets.ModelViewSet):
    model = Bank
    serializer_class = BankSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Bank.objects.all()


class PaycheckView(viewsets.ModelViewSet):
    model = Paycheck
    serializer_class = PaycheckSerializer
    renderer_classes = (PmsJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    queryset = Paycheck.objects.all()


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def set_profile_image(request):
    try:
        logger.info('trying to set %s profile image.' % request.user)
        employee = Employee.objects.get(user=request.user)
        employee.image = request.FILES['image']
        employee.save()
        logger.info('%s profile image updated successfully.' % request.user)
        return PmsResponse(
            {"msg": "Profile image save successfully."},
            status=status.HTTP_200_OK,
        )
    except Employee.DoesNotExist:
        logger.warning('%s employee profile not exists.' % request.user)
        return PmsResponse(
            {"msg": "Employee not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to set %s profile image.' % request.user)
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to set employee profile image."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def search_employee(request):
    try:
        logger.info('available employees searching...')
        employees = Employee.objects.filter(availability=EMPLOYMENT_AVAILABILITY.available) or Employee.objects.none()
        logger.info('employee getting successfully.')
        return PmsResponse(
            EmployeeProfileSerializer(instance=employees, many=True).data,
            status=status.HTTP_200_OK,
        )

    except Exception as ex:
        logger.error('failed to search available employee.')
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to search employee."},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def employee_details(request):
    try:
        logger.info('trying to get %s employee full profile.' % request.user)
        employee = Employee.objects.get(user=request.user)
        logger.info('%s employee full profile getting successfully.' % request.user)
        return PmsResponse(
            EmployeeDetailsSerializer(instance=employee).data,
            status=status.HTTP_200_OK,
        )
    except Employee.DoesNotExist:
        logger.warning('%s employee profile not exists.' % request.user)
        return PmsResponse(
            {"msg": "Employee not exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as ex:
        logger.error('failed to get %s employee profile.' % request.user)
        logger.exception(ex)
        return PmsResponse(
            {"msg": "Failed to get employee full profile."},
            status=status.HTTP_400_BAD_REQUEST,
        )
