# tests.py
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import ChatRoom
from .serializers import ChatRoomSerializer

class ChatRoomViewSetTests(APITestCase):

    def setUp(self):
        # Create some ChatRoom instances for testing
        self.chatroom1 = ChatRoom.objects.create(name='Room 1')
        self.chatroom2 = ChatRoom.objects.create(name='Room 2')
        self.client = APIClient()

    def test_list_chatrooms(self):
        # Test the listing of chat rooms
        response = self.client.get(reverse('chatroom-list'))
        chatrooms = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(chatrooms, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_chatroom(self):
        # Test retrieving a single chat room
        response = self.client.get(reverse('chatroom-detail', args=[self.chatroom1.id]))
        chatroom = ChatRoom.objects.get(id=self.chatroom1.id)
        serializer = ChatRoomSerializer(chatroom)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_chatroom(self):
        # Test creating a new chat room
        data = {'name': 'Room 3'}
        response = self.client.post(reverse('chatroom-list'), data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 3)
        self.assertEqual(ChatRoom.objects.get(id=response.data['id']).name, 'Room 3')

    def test_update_chatroom(self):
        # Test updating an existing chat room
        data = {'name': 'Updated Room 1'}
        response = self.client.put(reverse('chatroom-detail', args=[self.chatroom1.id]), data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChatRoom.objects.get(id=self.chatroom1.id).name, 'Updated Room 1')

    def test_delete_chatroom(self):
        # Test deleting a chat room
        response = self.client.delete(reverse('chatroom-detail', args=[self.chatroom1.id]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatRoom.objects.count(), 1)