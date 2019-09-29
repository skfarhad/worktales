from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.story.models import Story, Comment
from apps.user.models import User
from apps.workplace.models import Workplace
from apps.story.urls import STORY_ULRS

client = APIClient()

story_prefix = '/v0/story/'


def create_user(username):
    user = User.objects.create(
        username=username, is_active=True,
        full_name='User1',
    )
    return user


def create_workplace(user, name, members):
    workplace = Workplace.objects.create(
        owner=user,
        name=name,
    )
    workplace.members.add(*members)
    workplace.save()
    return workplace


def create_story(user, msg='Hello world..', wp=None):
    story = Story(
        body=msg,
        creator=user,
        workplace=wp
    )
    story.save()
    return story


class StoryTestCase(TestCase):

    def setUp(self):
        self.valid_access_token1 = ''
        self.username1 = 'username1'
        self.username2 = 'username2'
        self.username3 = 'username3'
        self.username4 = 'username4'
        self.username5 = 'username5'
        self.username6 = 'username6'
        self.username7 = 'username7'
        self.username8 = 'username8'
        self.username9 = 'username9'
        self.username10 = 'username10'

    def test_create_story_success(self):
        user1 = create_user(self.username1)
        wp1 = create_workplace(user1, 'WP1', [])

        # story = create_story(user1, 'Hello...', wp1)
        # print(story.id)

        client.force_authenticate(user1)

        response = client.post(
            story_prefix + STORY_ULRS['story'],
            {
                'body': 'hello world1.........',
                'images': ['dasdfasdf'],
                'workplace': wp1.id
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post(
            story_prefix + STORY_ULRS['story'],
            {
                'body': 'hello world2.........',
                'images': ['dasdfasdf'],
                'workplace': wp1.id
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_story_fail_auth(self):
        user1 = create_user(self.username1)
        wp1 = create_workplace(user1, 'WP1', [])

        response = client.post(
            story_prefix + STORY_ULRS['story'],
            {
                'body': 'hello world2.........',
                'images': ['dasdfasdf'],
                'workplace': wp1.id
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_story_fail_blank_workplace(self):
        user1 = create_user(self.username1)
        # wp1 = create_workplace(user1, 'WP1', [])

        client.force_authenticate(user1)

        response = client.post(
            story_prefix + STORY_ULRS['story'],
            {
                'body': 'hello blank workplace!',
                'images': ['dasdfasdf'],
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_story_success(self):
        user1 = create_user(self.username1)
        wp1 = create_workplace(user1, 'WP1', [])

        story = create_story(user1)

        client.force_authenticate(user1)

        response = client.patch(
            story_prefix + STORY_ULRS['story_id'].replace('<uuid:pk>', str(story.id)),
            {
                'body': 'Hello world 2...',
                'images': ['asdfasdf'],
                'workplace': wp1.id
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_story_fail_permission(self):
        user1 = create_user(self.username1)
        user2 = create_user(self.username2)
        wp1 = create_workplace(user1, 'WP1', [])

        story = create_story(user2, 'hello....', wp1)

        client.force_authenticate(user1)

        response = client.patch(
            story_prefix + STORY_ULRS['story_id'].replace('<uuid:pk>', str(story.id)),
            {
                'body': 'Hello world 2...',
                'images': ['asdfasdf'],
                'workplace': wp1.id
            },
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_story_list(self):
        user1 = create_user(self.username1)
        user2 = create_user(self.username2)
        user3 = create_user(self.username3)

        wp1 = create_workplace(user1, 'WP1', [user2])
        wp2 = create_workplace(user3, 'WP1', [])
        story1 = create_story(user1, 'WP1 us1....', wp1)
        story2 = create_story(user1, 'WP1 us2....', wp1)
        story3 = create_story(user3, 'WP2 us3....', wp2)

        client.force_authenticate(user2)

        response = client.get(
            story_prefix + STORY_ULRS['story'],
            {

            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
