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
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user2
        )
        self.client.force_authenticate(user1)
        response = self.client.get(reverse('todo_app:task-list'))
        owner = user1
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# GET: /task/?completed=[True/Flase]/$
class GetTaskListCompleted(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_list_completed(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get('http://testserver/task/?completed=True')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list_completed(self):
        """Test retrieving a list of tasks with owner is the who login"""
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=user1
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=user1
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=user2
        )
        self.client.force_authenticate(user1)
        response = self.client.get('http://testserver/task/?completed=True')
        owner = user1
        tasks = Task.objects.filter(owner_id=owner, completed=True)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


# GET: /task/?search=<title of task, description of task>[a-zA-Z0-9]+/$
class GetTaskListSearch(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_list_completed(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get('http://testserver/task/?completed=True')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list_completed(self):
        """Test retrieving a list of tasks with owner is the who login"""
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=user1
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=user1
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=user2
        )
        self.client.force_authenticate(user1)
        response = self.client.get('http://testserver/task/?completed=True')
        owner = user1
        tasks = Task.objects.filter(owner_id=owner, completed=True)
        serializer = TaskSerializer(tasks, many=True)
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
            'task_name': '00000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000',
            'task_desc': '',
        }
        response = self.client.post(reverse('todo_app:task-list'), new_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)

# GET: /task/<id>[0-9+]
class GetTaskDetail(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required_task_detail(self):
        """Test that login is required to access the endpoint"""
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            owner=user1
        )
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_detai_success(self):
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.task1=Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            owner=user1
        )
        self.task2=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        self.task3=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user2
        )
        self.client.force_authenticate(user1)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_retrieve_task_detai_unsuccess_with_wrong_owner(self):
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.task1=Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            owner=user1
        )
        self.task2=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        self.task3=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user2
        )
        self.client.force_authenticate(user2)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_retrieve_task_detai_unsuccess_with_id_not_exist(self):
        user1 = User.objects.create_user(
            'test1',
            'testpass'
        )
        self.task1=Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            owner=user1
        )
        self.task2=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user1
        )
        user2 = User.objects.create_user(
            'test2',
            'testpass'
        )
        self.task3=Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            owner=user2
        )
        self.client.force_authenticate(user2)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': '30'}))
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


