from rest_framework import viewsets
from rest_framework import filters
import django_filters.rest_framework
from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.http import HttpResponse, HttpResponseRedirect

class TaskViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    # only Authenticated User can perform CRUD operation
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()  # use filter and ordering so remove order_by
    serializer_class = TaskSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ('completed',)  # category task by attribute `completed`
    ordering = ('date_created',)  # sorting by date_create
    search_fields = ('task_name', 'task_desc',)  # search for each column of db

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
    # 1st way normal deal with small deletion
    # Task.objects.all().delete()
    # 2nd way fastest deal with bulk deletion
    # task = Task.objects.all()
    # if task.exists():
    #     task._raw_delete(task.db)
    # return Response(status=status.HTTP_204_NO_CONTENT)
    # return HttpResponseRedirect(redirect_to='https://google.com')
    # return HttpResponse("Deleted!", status=302)
    owner = request.user
    Task.objects.filter(owner_id=owner).delete()
    return HttpResponseRedirect(redirect_to='/task/')
