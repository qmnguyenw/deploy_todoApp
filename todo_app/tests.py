from django.test import TestCase
from rest_framework.test import APIClient
import json
from rest_framework import response, status
from django.urls import reverse
from .models import Task
from .serializers import TaskSerializer
from .views import *
from django.contrib.auth.models import User

class PublicTasksApiTests(TestCase):
    """Test the publicly available tasks API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(reverse('todo_app:task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTasksApiTests(TestCase):
    """Test the private tasks API"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='GetAllTasksTest1 test description',
            completed='True',
        )
        self.user = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='GetAllTasksTest2 test description',
            completed='True',
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='GetAllTasksTest3 test description',
            completed='True',
        )

    def test_retrieve_task_list(self):
        """Test retrieving a list of tasks"""
        response = self.client.get(reverse('todo_app:task-list'))
        owner = self.user
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_task_successful(self):
        """Test create a new task"""
        new_task = {
            'task_name': 'Test GetAllTasksTest3',
            'task_desc': 'GetAllTasksTest3 test description',
            'date_created': '',
            'completed': 'False',
            'doc': '',
            'image': '',
            # 'owner': ''
        }
        self.client.post(reverse('todo_app:task-list'),new_task)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_task_unsuccessful_with_unvalid(self):
        """Test create a new task"""
        new_task = {
            'task_name': 'Test GetAllTasksTest3',
            'task_desc': 'GetAllTasksTest3 test description',
            'date_created': '',
            'completed': '',
            'doc': '',
            'image': '',
            # 'owner': ''
        }
        self.client.post(reverse('todo_app:task-list'),new_task)
        # exists = Task.objects.filter(
        #     owner=self.user,
        #     task_name=new_task['task_name'],
        # ).exists()
        # self.assertTrue(exists)
        self.assertEqual(response.status, status.HTTP_400_BAD_REQUEST)

    # def test_create_task_invalid(self):
    #     """Test creating invalid task fails"""
    #     payload = {'name': ''}
    #     response = self.client.post(reverse('task-list'), payload)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_tasks_assigned_to_recipes(self):
    #     """Test filtering tasks by those assigned to recipes"""
    #     task1 = Task.objects.create(
    #         user=self.user, name='Apples'
    #     )
    #     task2 = Task.objects.create(
    #         user=self.user, name='Turkey'
    #     )
    #     recipe = Recipe.objects.create(
    #         title='Apple crumble',
    #         time_minutes=5,
    #         price=10,
    #         user=self.user
    #     )
    #     recipe.tasks.add(task1)

    #     response = self.client.get(reverse('task-list'), {'assigned_only': 1})

    #     serializer1 = TaskSerializer(task1)
    #     serializer2 = TaskSerializer(task2)
    #     self.assertIn(serializer1.data, response.data)
    #     self.assertNotIn(serializer2.data, response.data)

    # def test_retrieve_tasks_assigned_unique(self):
    #     """Test filtering tasks by assigned returns unique items"""
    #     task = Task.objects.create(user=self.user, name='Eggs')
    #     Task.objects.create(user=self.user, name='Cheese')
    #     recipe1 = Recipe.objects.create(
    #         title='Eggs benedict',
    #         time_minutes=30,
    #         price=12.00,
    #         user=self.user
    #     )
    #     recipe1.tasks.add(task)
    #     recipe2 = Recipe.objects.create(
    #         title='Coriander eggs on toast',
    #         time_minutes=20,
    #         price=5.00,
    #         user=self.user
    #     )
    #     recipe2.tasks.add(task)

    #     response = self.client.get(reverse('task-list'), {'assigned_only': 1})

    #     self.assertEqual(len(response.data), 1)
