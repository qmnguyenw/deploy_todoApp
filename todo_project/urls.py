from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
# from todoApp import views
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# router = routers.DefaultRouter()
# router = routers.SimpleRouter()
# router.register(r'task', views.TaskViewSet, basename='task')
# router.register(r'due_task', views.DueTaskViewSet)
# router.register(r'completed_task', views.CompletedTaskViewSet)

# urlpatterns = [
#     url(r'^', include(router.urls), name='main'),
#     url(r'^delete-all/', views.deleteAll, name='deleteall'),
#     url(r'^admin/', admin.site.urls),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     url(r'^register/$', views.CreateUserView.as_view(), name='user'),
# ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

schema_view = get_schema_view(
    openapi.Info(
        title="To Do Application API",
        default_version="",
        description="To Do Application API Description",
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # url for admin page
    url(r'^admin/', admin.site.urls),
    # url for login - logout
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url for apps
    path('task/', include('todo_app.urls', namespace='todo_app')),
    url(r'^user/', include('users.urls', namespace='user')),
    # url document api (redoc, swagger)
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
