from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=50, unique=True)
    team = models.ForeignKey(
        'team.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name="user_team")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email', 'password']

    def is_creator(self):
        if self.team and self.team.creator_id == self.id:
            return True
        return False
