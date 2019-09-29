from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from apps.common.serializers import CustomSerializer
from .models import Story, Comment


class StorySerializer(CustomSerializer):
    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'workplace': {'required': True}}

    def update_obj(self, instance, validated_data):
        if instance.creator != self.context['request'].user:
            raise PermissionDenied(detail='Not allowed!')
        return super().update_obj(instance, validated_data)


class CommentSerializer(CustomSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id',)
