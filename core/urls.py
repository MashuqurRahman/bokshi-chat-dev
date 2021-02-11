# core/urls.py
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

# from core.apis.group_chat import (ChatGroupDetailview,
#                                   ChatGroupMessageDetailView,
#                                   ChatGroupMessageView, ChatGroupView,
#                                   MessageModelViewSet, UserModelViewSet)
from core.apis.group_chat import MessageModelViewSet, UserModelViewSet
from core.apis.user_chat import UserChatCreateAPI
from core.apis.user import UserListAPI, UserRetrieveAPI
from core.apis.user_chat import UserChatListAPI

# from .views import group_view

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
# router.register(r'group', GroupMessageView, basename='group-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('api/users/', UserListAPI.as_view(), name='users'),
    path('api/user/<int:pk>/', UserRetrieveAPI.as_view(), name='user'),
    path('api/chat/messages/', UserChatListAPI.as_view(), name='user_chat'),
    path('api/chat/create/', UserChatCreateAPI.as_view(), name='user_chat_create'),
    # path('chat/groups/', ChatGroupView.as_view(), name='chat_groups'),
    # path('chat/<int:pk>/group/', ChatGroupDetailview.as_view(), name='chat_group'),
    # path(
    #     'chat/messages/',
    #     ChatGroupMessageView.as_view(),
    #     name='chat_group_messages',
    # ),
    # path(
    #     'chat/<str:group_name>/messages/',
    #     ChatGroupMessageView.as_view(),
    #     name='chat_group_name_messages',
    # ),
    # path(
    #     'chat/<int:pk>/message/',
    #     ChatGroupMessageDetailView.as_view(),
    #     name='chat_group_message',
    # ),
    # path('group/', group_view, name='groups'),
    path(
        '',
        login_required(TemplateView.as_view(template_name='core/chat.html')),
        name='home',
    ),
]
