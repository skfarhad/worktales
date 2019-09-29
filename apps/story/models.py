import uuid
from django.db import models
# from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

from apps.user.models import User
from apps.workplace.models import Workplace
from apps.common.models import TimeFields


class Story(models.Model):
    PRIVACY_CHOICES = (
        (0, 'Self'),
        (1, 'Friends'),
        (2, 'Public'),
    )

    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Verified'),
        (2, 'Rejected'),
    )

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    time_created = models.DateTimeField(default=timezone.now)
    time_updated = models.DateTimeField(auto_now=True)

    body = models.TextField(blank=True, null=True)

    link = models.URLField(blank=True, null=True)
    attachment = JSONField(blank=True, null=True)
    images = JSONField(blank=True, null=True)

    creator = models.ForeignKey(
        User, null=True,
        on_delete=models.CASCADE,
        related_name='story_user'
    )

    workplace = models.ForeignKey(
        Workplace, null=True,
        on_delete=models.SET_NULL,
        related_name='story_workplace'
    )

    claps = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    privacy_level = models.PositiveSmallIntegerField(choices=PRIVACY_CHOICES, default=2)

    def __str__(self):
        return self.id


class Comment(TimeFields):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    body = models.TextField(blank=True)

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='comment_user'
    )

    link = models.URLField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    claps = models.PositiveIntegerField(default=0)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_comment')


