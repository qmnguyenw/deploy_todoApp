from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import *

app_name = 'task'

router = routers.DefaultRouter()
router.register(r'', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^delete-all', deleteAll, name='delete-all')
]
