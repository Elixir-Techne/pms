from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from .models import Task, TaskCategory


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id', 'project', 'title', 'category', 'description', 'creator', 'assign', 'start_date', 'end_date',
            'billing_method', 'status', 'effort'
        )
        read_only = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ('id', 'name', 'description')
        read_only = ('id',)
