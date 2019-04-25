from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from .models import Contract, ContractDocument


class ContractDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractDocument
        fields = (
            'id', 'contract', 'title', 'created', 'image')
        read_only = ('id',)


class ContractSerializer(serializers.ModelSerializer):
    documents = ContractDocumentSerializer(many=True, read_only=True, source='contract_document')

    class Meta:
        model = Contract
        fields = (
            'id', 'employee', 'client', 'description', 'payment_mode', 'documents')
        read_only = ('id',)
