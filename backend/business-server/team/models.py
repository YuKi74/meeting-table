import uuid

from django.db import models
from user.models import User


class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    creator = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=False, blank=False, related_name="team_creator")
    introduction = models.CharField(max_length=255)
    uuid = models.UUIDField(
        max_length=32, default=uuid.uuid4)


class Application(models.Model):

    class Status(models.TextChoices):
        ACCEPTED = 'yes'
        DENIED = 'no'
        PENDING = 'unsolved'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8, default=Status.PENDING, choices=Status.choices)


class MeetingRoom(models.Model):
    id = models.BigAutoField(primary_key=True)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    uuid = models.UUIDField(max_length=32, default=uuid.uuid4)
    team = models.ForeignKey(to=Team, on_delete=models.CASCADE)


class MeetingRoomFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    meetingRoom = models.ForeignKey(to=MeetingRoom, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    files = models.FileField(upload_to='')
    time = models.DateField(auto_now_add=True)
