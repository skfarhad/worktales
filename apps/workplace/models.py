import uuid
from django.db import models
from apps.user.models import User
from apps.common.models import TimeFields


class Workplace(TimeFields):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=64, blank=False)
    owner = models.OneToOneField(
        User, null=True, on_delete=models.SET_NULL, related_name='owner_user'
    )
    members = models.ManyToManyField(
        User, blank=True, related_name='member_user'
    )

    def __str__(self):
        return self.name
