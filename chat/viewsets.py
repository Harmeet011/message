from rest_framework import viewsets
from django.contrib.auth import authenticate
from chat.models import ChatRoom, Message
from chat.serializers import ChatRoomSerializer, MessageSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

class ChatRoomViewSets(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSets(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super(RegisterView, self).create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        if not user.is_active:
            user.is_active = True
            user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': response.data,
            'token': token.key
        })
    
class LoginView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)