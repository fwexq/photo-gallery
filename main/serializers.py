from rest_framework import serializers

from main.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description', 'created_at', 'updated_at', 'status', 'publish', 'photo', 'get_absolute_url', 'author', 'liked' )