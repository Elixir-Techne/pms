from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from .models import Manager


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = (
            'id', 'user', 'first_name', 'last_name', 'ssn', 'phone', 'status'
        )
        read_only = ('id',)
