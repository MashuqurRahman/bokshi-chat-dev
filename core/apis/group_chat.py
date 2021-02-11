from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import CharField, ModelSerializer

from core.models import ChatGroup, ChatGroupMessage, MessageModel


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username']
        )
        msg = MessageModel(recipient=recipient, body=validated_data['body'], user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


# class ChatGroupSerializer(ModelSerializer):
#     class Meta:
#         model = ChatGroup
#         fields = ('name', 'member')


# class ChatGroupDetailSerializer(ModelSerializer):
#     class Meta:
#         model = ChatGroup
#         fields = "__all__"


# class ChatGroupMessageSerializer(ModelSerializer):
#     class Meta:
#         model = ChatGroupMessage
#         fields = "__all__"


# class ChatGroupMessageDetailSerializer(ModelSerializer):
#     class Meta:
#         model = ChatGroupMessage
#         fields = "__all__"

# core/api.py

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat import settings
from core.models import ChatGroup, ChatGroupMessage, MessageModel
# from core.serializers import (ChatGroupDetailSerializer,
#                               ChatGroupMessageDetailSerializer,
#                               ChatGroupMessageSerializer, ChatGroupSerializer,
#                               MessageModelSerializer, UserModelSerializer)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """

    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(
            Q(recipient=request.user) | Q(user=request.user)
        )
        target = self.request.query_params.get('target', None)
        # if group_name is not None:
        #     self.queryset = self.queryset.filter()
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__username=target)
                | Q(recipient__username=target, user=request.user)
            )
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(
                Q(recipient=request.user) | Q(user=request.user), Q(pk=kwargs['pk'])
            )
        )
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)


# class ChatGroupView(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = ChatGroup.objects.all()
#     serializer_class = ChatGroupSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ChatGroupDetailview(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):
#     queryset = ChatGroup.objects.all()
#     serializer_class = ChatGroupDetailSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class ChatGroupMessageView(
#     mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
# ):
#     queryset = ChatGroupMessage.objects.all()
#     serializer_class = ChatGroupMessageSerializer

#     def get(self, request, *args, **kwargs):
#         group_name = self.kwargs.get('group_name', None)
#         # print(group_name)
#         # if group_name is not None:
#         #     self.queryset = self.get_queryset().filter(group_name=group_name)
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ChatGroupMessageDetailView(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):

#     queryset = ChatGroupMessage.objects.all()
#     serializer_class = ChatGroupMessageDetailSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
