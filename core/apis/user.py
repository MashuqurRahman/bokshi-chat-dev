# core/apis/user.py

from django.contrib.auth.models import User
from rest_framework import generics

from core.serializers.user import UserListSerializer, UserRetrieveSerializer


class UserListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRetrieveAPI(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
