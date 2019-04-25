from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from apps.masters.models import City, Country, State
from apps.masters.serializers import CityRelatedField, StateRelatedField, CountryRelatedField
from .models import Employee, EmploymentCompensation, Bank, Paycheck


class EmployeeProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    city = CityRelatedField(queryset=City.objects.all())
    country = CountryRelatedField(queryset=Country.objects.all())
    state = StateRelatedField(queryset=State.objects.all())

    class Meta:
        model = Employee
        fields = (
            'id', 'user', 'image', 'first_name',
            'last_name', 'gender', 'ssn', 'birth_date', 'address_1', 'address_2',
            'country', 'state', 'city', 'zip_code', 'phone', 'status', 'availability', 'email'
        )
        read_only = ('id', 'image',)


class EmploymentCompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentCompensation
        fields = (
            'id', 'employee', 'company', 'location', 'title', 'start_date', 'end_date', 'department',
            'compensation_type', 'employment_type', 'annual_salary', 'job_duties', 'flsa_classification', 'manager',
            'direct_reports', 'is_current', 'notes'
        )
        read_only = ('id',)


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = (
            'id', 'employee', 'type', 'routing_number', 'account_number', 'name', 'address', 'notes'
        )
        read_only = ('id',)


class PaycheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paycheck
        fields = (
            'id', 'method', 'distribution', 'notes'
        )
        read_only = ('id',)


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    compensations = EmploymentCompensationSerializer(many=True)
    bank = BankSerializer(many=True)
    paycheck = PaycheckSerializer(many=True)
    city = CityRelatedField(queryset=City.objects.all())
    country = CountryRelatedField(queryset=Country.objects.all())
    state = StateRelatedField(queryset=State.objects.all())

    class Meta:
        model = Employee
        fields = (
            'id', 'user', 'image', 'gender', 'ssn', 'birth_date', 'address_1', 'address_2',
            'country', 'state', 'city', 'zip_code', 'phone', 'status', 'availability',
            'compensations', 'bank', 'paycheck'
        )
