# core/apis/user_chat.py
from django.shortcuts import redirect
from rest_framework import generics, mixins

from core.models import MessageModel
from core.serializers.user_chat import UserChatListSerializer


class UserChatListAPI(generics.ListAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = UserChatListSerializer

    def list(self, request, *args, **kwargs):
        # breakpoint()
        # self.queryset = self.queryset.filter(
        #     Q(recipient=request.user) | Q(user=request.user)
        # )
        target = self.request.query_params.get('target', None)
        # # if group_name is not None:
        # #     self.queryset = self.queryset.filter()
        # if target is not None:
        #     self.queryset = self.queryset.filter(
        #         Q(recipient=request.user, user__username=target)
        #         | Q(recipient__username=target, user=request.user)
        if target is not None:
            self.queryset = self.queryset.filter(recipient__username=target)
        return super(UserChatListAPI, self).list(request, *args, **kwargs)


class UserChatCreateAPI(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = MessageModel.objects.all()
    serializer_class = UserChatListSerializer

    def post(self, request, *args, **kwargs):
        # breakpoint()
        return self.create(request, *args, **kwargs)
