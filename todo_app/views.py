import django_filters.rest_framework
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import filters, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    # authentication_classes = (BasicAuthentication, SessionAuthentication)
    # only Authenticated User can perform CRUD operation
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()  # use filter and ordering so remove order_by
    serializer_class = TaskSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('completed',)  # filter tasks by attribute `completed`
    ordering = ('date_created',)  # sorting
    search_fields = ('task_name', 'task_desc',) # searching

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the tasks
        for the currently authenticated user.
        """
        owner = self.request.user
        return Task.objects.filter(owner_id=owner)


def deleteAll(request):
    permission_classes = (IsAuthenticated,)
    if request.user.is_authenticated:
        owner = request.user
        Task.objects.filter(owner_id=owner).delete()
    return HttpResponseRedirect(redirect_to='/task/')
