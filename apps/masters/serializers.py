from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from .models import Country, State, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class CityRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return City.objects.get(pk=data)


class CountryRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return Country.objects.get(pk=data)


class StateRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return State.objects.get(pk=data)
