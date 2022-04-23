from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import (Comment,
                          Follow,
                          Group,
                          Post,
                          User)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    def validate_following(self, value):
      user = self.context['request'].user
      if (value == user 
          or Follow.objects.filter(user=user, following=value).exists()):
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!')
        return value

    class Meta:
        fields = '__all__'
        model = Follow
