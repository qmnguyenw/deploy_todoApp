from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

app_name = 'users'

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='user-main')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
