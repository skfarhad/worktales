import uuid
from django.contrib.gis.db import models
from django.utils import timezone

# from django.contrib.gis.geos import Point


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

    body = models.TextField(blank=True)

    link = models.URLField(null=True)
    attachment = models.URLField(null=True)
    images = models.URLField(null=True)

    claps = models.PositiveIntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    privacy_level = models.PositiveSmallIntegerField(choices=PRIVACY_CHOICES, default=0)

    def __str__(self):
        return self.id


class Comment(models.Model):

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    time_created = models.DateTimeField(default=timezone.now)
    body = models.TextField(blank=True)

    link = models.URLField(null=True)
    images = models.URLField(null=True)
    claps = models.PositiveIntegerField(default=0)

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_comment')


