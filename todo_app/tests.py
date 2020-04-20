from .views import *
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
import json
from django.urls import reverse
from rest_framework import status, response, request

'''GET: /task/'''


class GetTaskList(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_login_required_task_list(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(reverse('todo_app:task-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list(self):
        """Test retrieving a list of tasks with owner is the who login"""
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('todo_app:task-list'))
        owner = self.user1
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        data_total = response.data['results']
        while response.data['next']!=None:
            response = self.client.get(response.data['next'])
            data_total += response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)
        # fix when pagination
        self.assertEqual(data_total, serializer.data)


'''GET: /task/?completed=[True/Flase]/$'''


class GetTaskListCompleted(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_login_required_task_list_completed(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get('http://testserver/task/?completed=True')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list_completed(self):
        """Test retrieving a list of tasks with owner is the who login"""
        self.client.force_authenticate(self.user1)
        response = self.client.get('http://testserver/task/?completed=True')
        owner = self.user1
        tasks = Task.objects.filter(owner_id=owner, completed=True)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)


'''GET: /task/?search=<title of task, description of task>[a-zA-Z0-9]+/$'''


class GetTaskListSearch(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1 TestDemo',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2 TestDemo',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4 TestDemo',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_login_required_task_list_completed(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get('http://testserver/task/?search=TestDemo')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_list_completed(self):
        """Test retrieving a list of tasks with owner is the who login"""
        self.client.force_authenticate(self.user1)
        response = self.client.get('http://testserver/task/?search=TestDemo')
        owner = self.user1
        tasks = Task.objects.filter(
            owner_id=owner, task_name__contains='TestDemo')
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)


'''POST: /task/'''


class CreateTask(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_task_unsuccessful_without_authentication(self):
        """Test create task without authentication"""
        new_task = {
            'task_name': 'Test CreateTaskTest',
            'task_desc': 'test description',
        }
        response = self.client.post(reverse('todo_app:task-list'), data=new_task)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exists = Task.objects.filter(
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)

    def test_create_task_successful(self):
        """Test create a new task successful"""
        self.user = User.objects.create_user(
            'test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': 'Test GetAllTasksTest3',
            'task_desc': 'GetAllTasksTest3 test description',
        }
        response = self.client.post(reverse('todo_app:task-list'), data=new_task)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertTrue(exists)

    def test_create_task_unsuccessful_with_missing_mandatory_information(self):
        """Test create a new task unsuccessful with missing mandatory information"""
        self.user = User.objects.create_user(
            'test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': 'f',  # required atrribute, cannot null
            'task_desc': '',  # required atrribute, cannot null
        }
        response = self.client.post(reverse('todo_app:task-list'), data=new_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)

    def test_create_task_unsuccessful_with_wrong_data_type_range(self):
        """Test create a new task unsuccessful with wrong data type/range"""
        self.user = User.objects.create_user(
            'test',
            password='testpass'
        )
        self.client.force_authenticate(self.user)
        new_task = {
            'task_name': '00000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000',
            'task_desc': '',
        }
        response = self.client.post(reverse('todo_app:task-list'), data=new_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exists = Task.objects.filter(
            owner=self.user,
            task_name=new_task['task_name'],
        ).exists()
        self.assertFalse(exists)


'''GET: /task/<id>[0-9+]'''


class GetTaskDetail(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_login_required_task_detail(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_task_detai_success(self):
        """Test get task detail success"""
        self.client.force_authenticate(self.user1)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_task_detai_unsuccess_with_wrong_owner(self):
        """Test get task detail unsuccess with wrong owner"""
        self.client.force_authenticate(self.user2)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_task_detai_unsuccess_with_id_not_exist(self):
        """Test get task detail unsuccess with id not exist"""
        self.client.force_authenticate(self.user2)
        response = self.client.get(
            reverse('todo_app:task-detail', kwargs={'pk': '30'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

'''PUT: /task/<id>[0-9+]'''


class UpdateTaskDetail(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_update_task_unsuccessful_without_authentication(self):
        """Test update task without authentication"""
        update_task = {
            'task_name': 'Test Update',
            'task_desc': 'test update',
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_task_success(self):
        """Test update task success"""
        self.client.force_authenticate(self.user1)
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        update_task = {
            'task_name': 'Test Update',
            'task_desc': 'test update',
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(pk=self.task1.pk)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)

    def test_update_task_unsuccess_id_not_exist(self):
        """Test update task unsuccess with id not exist"""
        self.client.force_authenticate(self.user1)
        update_task = {
            'task_name': 'Test Update',
            'task_desc': 'test update',
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': '30'}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_detai_unsuccess_with_wrong_owner(self):
        """Test update new task unsuccess with wrong owner"""
        self.client.force_authenticate(self.user2)
        update_task = {
            'task_name': 'Test Update',
            'task_desc': 'test update',
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_unsuccessful_with_missing_mandatory_information(self):
        """Test update a new task unsuccessful with missing mandatory information"""
        self.client.force_authenticate(self.user1)
        update_task = {
            'task_name': 'f',  # required atrribute, cannot null
            'task_desc': '',  # required atrribute, cannot null
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_unsuccessful_with_wrong_data_type_range(self):
        """Test update a new task"""
        self.client.force_authenticate(self.user1)
        update_task = {
            'task_name': '00000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000\
            0000000000000000000000000000000000000000000000000000000000000000000000',
            'task_desc': '',
        }
        response = self.client.put(reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}), data=update_task)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

'''DELETE: /task/<id>[0-9+]'''


class DeleteTaskDetail(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_login_required_task_detail(self):
        """Test that login is required to access the endpoint"""
        response = self.client.delete(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task_detai_success(self):
        """Test delete task detail success"""
        self.client.force_authenticate(self.user1)
        task_delete_name=self.task1.task_name
        response = self.client.delete(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        exists = Task.objects.filter(
            task_name=task_delete_name,
        ).exists()
        self.assertFalse(exists)

    def test_delete_task_detai_unsuccess_with_wrong_owner(self):
        """Test delete task detail unsuccess with wrong owner"""
        self.client.force_authenticate(self.user2)
        task_delete_name=self.task1.task_name
        response = self.client.delete(
            reverse('todo_app:task-detail', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        exists = Task.objects.filter(
            task_name=task_delete_name,
        ).exists()
        self.assertTrue(exists)

    def test_retrieve_task_detai_unsuccess_with_id_not_exist(self):
        """Test get task detail unsuccess with id not exist"""
        self.client.force_authenticate(self.user2)
        response = self.client.delete(
            reverse('todo_app:task-detail', kwargs={'pk': '30'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

'''GET: /task/delete-all'''
class DeleteAllTask(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            'test1',
            password='testpass'
        )
        self.task1 = Task.objects.create(
            task_name='Test GetAllTasksTest1',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.task2 = Task.objects.create(
            task_name='Test GetAllTasksTest2',
            task_desc='test description',
            completed='False',
            owner=self.user1
        )
        self.task3 = Task.objects.create(
            task_name='Test GetAllTasksTest3',
            task_desc='test description',
            completed='True',
            owner=self.user1
        )
        self.user2 = User.objects.create_user(
            'test2',
            password='testpass'
        )
        self.task4 = Task.objects.create(
            task_name='Test GetAllTasksTest4',
            task_desc='test description',
            completed='True',
            owner=self.user2
        )

    def test_delete_task_list_success(self):
        """Test that login is required to access the endpoint"""
        self.client.login(username='test1', password='testpass')
        response = self.client.get('/task/delete-all')
        owner = self.user1
        tasks = Task.objects.filter(owner_id=owner)
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual([],serializer.data)
        tasks_user2 = Task.objects.filter(owner_id=self.user2)
        serializer_user2 = TaskSerializer(tasks_user2, many=True)
        self.assertNotEqual([], serializer_user2.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        