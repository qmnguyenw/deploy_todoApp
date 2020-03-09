from .views import *
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
import json
from django.urls import reverse
from rest_framework import status, response

# GET: /task/
class GetTaskList(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_list(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(reverse('todo_app:task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list(self):
        """Test retrieving a list of tasks with owner is the who login"""
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
        )
        self.user = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
        )

        response = self.client.get(reverse('todo_app:task-list'))
        owner = self.user
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class CreateTask(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_task_unsuccessful_without_authentication(self):
        """Test create task without authentication"""
        new_task = {
            'task_name': 'Test CreateTaskTest',
            'task_desc': 'test description',
            'owner': ''
        }
        response = self.client.post(reverse('todo_app:task-list'), new_task)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exists = Task.objects.filter(
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)

    def test_create_task_successful(self):
        """Test create a new task"""
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': 'Test GetAllTasksTest3',
            'task_desc': 'GetAllTasksTest3 test description',
        }
        response = self.client.post(reverse('todo_app:task-list'), new_task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_task_unsuccessful_with_unvalid(self):
        """Test create a new task"""
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': 'f',  # required atrribute, cannot null
            'task_desc': '',  # required atrribute, cannot null
        }
        response = self.client.post(reverse('todo_app:task-list'), new_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)
