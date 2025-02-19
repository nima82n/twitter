from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'content', 'timestamp', 'likes']
        read_only_fields = ['user', 'timestamp']