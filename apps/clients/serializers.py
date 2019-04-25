from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from .models import Client, HireInvitation


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id', 'name', 'user', 'trade', 'description', 'email', 'address', 'contact_first_name', 'contact_last_name',
            'phone', 'status')
        read_only = ('id',)


class HireInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireInvitation
        fields = ('employee',)
