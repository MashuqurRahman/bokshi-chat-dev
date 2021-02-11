# core/serializers/user_chat.py
from rest_framework import serializers
from core.models import MessageModel


class UserChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = "__all__"
