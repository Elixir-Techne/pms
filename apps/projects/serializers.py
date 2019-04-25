from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from apps.masters.models import City, State, Country
from apps.masters.serializers import CityRelatedField, StateRelatedField, CountryRelatedField
from apps.tasks.serializers import TaskSerializer
from .models import Customer, Project, EmployeeProject


class CustomerSerializer(serializers.ModelSerializer):
    city = CityRelatedField(queryset=City.objects.all())
    country = CountryRelatedField(queryset=Country.objects.all())
    state = StateRelatedField(queryset=State.objects.all())

    class Meta:
        model = Customer
        fields = (
            'id', 'client', 'first_name', 'last_name', 'email', 'phone', 'country', 'state', 'city', 'zip_code',
            'status'
        )
        read_only = ('id',)


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='task_project')

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'description', 'customer', 'manager', 'billing_method', 'estimation', 'start_date',
            'end_date', 'members', 'status', 'tasks'
        )
        read_only = ('id', 'tasks')


class EmployeeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProject
        fields = (
            'id', 'employee', 'project', 'start_date', 'end_date', 'allocation'
        )
        read_only = ('id',)
