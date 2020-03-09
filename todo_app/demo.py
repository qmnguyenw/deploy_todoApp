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


class GetTaskList(TestCase):  # PublicTasksApiTests

    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_list(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(reverse('todo_app:task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list(self):
        """Test retrieving a list of tasks with owner is the who login"""
        # setup database
        # user1 = User.objects.create_user(
        #     'test',
        #     'testpass'
        # )
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        q = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            # owner=self.user
        )
        print(q.owner)
        user2 = User.objects.create_user(
            'test1',
            'testpass'
        )
        # self.client.force_authenticate(self.user)
        p = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user2
        )
        print(p.owner)
        # self.user=User.objects.get(username='test1')
        # self.client.force_authenticate(self.user)
        # get API response
        response = self.client.get(reverse('todo_app:task-list'))
        owner = self.user
        # get data from db
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        print(response.data)
        print(serializer.data)
        # test
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

# POST: /task/


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

    def test_create_task_unsuccessful_with_missing_mandatory_information(self):
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

    def test_create_task_unsuccessful_with_wrong_data_type_range(self):
        """Test create a new task"""
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            'task_desc': '',
        }
        response = self.client.post(reverse('todo_app:task-list'), new_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)


class GetTaskDetail(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_detail(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_detai(self):
        # setup db
        self.user = User.objects.create_user(
            'test',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
        )
        task = Task.objects.all()[0]
        # print(task.owner)
        self.user = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
        )
        task = Task.objects.all()[1]
        # print(task.owner)
        # self.user = User.objects.get(username='test')
        # self.client.force_authenticate(self.user)
        # get API response
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': 2}))
        owner = self.user
        # print(response.data)
        # print(owner)
        # get data from db
        # task = Task.objects.all()[1]
        # print(task)
        serializer = TaskSerializer(task, many=False)
        # test
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)

# class PrivateTasksApiTests(TestCase):
#     """Test the private tasks API"""

#     def setUp(self):

#         self.user = User.objects.create_user(
#             'test',
#             'testpass'
#         )
#         self.client.force_authenticate(self.user)
#         Task.objects.create(
#             task_name='Test GetAllTasksTest1',
#             task_desc='GetAllTasksTest1 test description',
#             completed='True',
#         )
#         self.user = User.objects.create_user(
#             'test1',
#             'testpass'
#         )
#         self.client.force_authenticate(self.user)
#         Task.objects.create(
#             task_name='Test GetAllTasksTest2',
#             task_desc='GetAllTasksTest2 test description',
#             completed='False',
#         )

#     def test_retrieve_task_list(self):
#         """Test retrieving a list of tasks"""
#         response = self.client.get(reverse('todo_app:task-list'))
#         owner = self.user
#         tasks = Task.objects.filter(owner_id=owner)
#         serializer = TaskSerializer(tasks, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)
