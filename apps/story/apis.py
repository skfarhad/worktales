from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Story, Comment
from apps.workplace.models import Workplace
from .serializers import StorySerializer, CommentSerializer

from apps.common.apis import CustomViewSet


class StoryViewset(CustomViewSet):
    permission_classes = [IsAuthenticated]
    ObjModel = Story
    ObjSerializer = StorySerializer

    def obj_filter(self, request):
        workplaces = Workplace.objects.filter(
            Q(members=request.user) |
            Q(owner=request.user)
        )
        workplaces = list(workplaces)
        # print(workplaces)
        obj_qs = Story.objects.filter(
            Q(workplace__in=workplaces)
        )
        return obj_qs


class CommentViewset(CustomViewSet):
    permission_classes = [IsAuthenticated]
    ObjModel = Comment
    ObjSerializer = CommentSerializer
