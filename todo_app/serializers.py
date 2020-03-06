from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

# create serializer


class TaskSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None, use_url=True, default='images/none/none.jpg')
    doc = serializers.FileField(
        max_length=None, use_url=True, default='docs/none/none.txt')
    # create owner to let permission
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'task_name', 'task_desc', 'completed',
                  'date_created', 'image', 'doc', 'owner')

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     # override Create method
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         user.save()
#         return user

#     class Meta:
#         model = User
#         fields = ('username', 'password')
#         extra_kwargs = {'password': {'write_only': True, 'required': True}}
