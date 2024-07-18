from django.urls import path
from rest_framework.routers import DefaultRouter
from chat.views import sumNumbersView
from chat.viewsets import ChatRoomViewSets, LoginView, MessageViewSets, RegisterView, UserViewSet

router = DefaultRouter()
router.register("chatroom", ChatRoomViewSets, basename="chatroom")
router.register('message', MessageViewSets, basename='message')
router.register(r'users', UserViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('sum_numbers/', sumNumbersView, name='sum_numbers'),
]
urlpatterns += [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]