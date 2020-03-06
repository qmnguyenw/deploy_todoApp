from rest_framework import viewsets

from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
