from rest_framework import routers
from django.urls import path

from .apis import StoryViewset, CommentViewset

STORY_ULRS = {
    'story_id': 'story/<uuid:pk>/',
    'story': 'story/',

    'comment_id': 'story/<uuid:pk>/',
    'comment': 'story/',

}

router = routers.DefaultRouter()
router.register('story', StoryViewset, base_name='story')
router.register('comment', CommentViewset, base_name='comment')


urlpatterns = [
    # path(STORY_ULRS['new_api'], NewAPI.as_view()),

]

urlpatterns += router.urls
