from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# create serializer
class TaskSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True, default='images/none/none.jpg')
    doc = serializers.FileField(
        max_length=None, use_url=True, default='docs/none/none.txt')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'task_name', 'task_desc', 'completed',
                  'date_created', 'image', 'doc', 'owner')
