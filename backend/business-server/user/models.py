from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=50)
    group = models.ForeignKey(
        'team.Team', on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['id', 'name', 'email']
    # password存储


# 写在类的函数和写在序列化器，还有写在view的函数由什么区别
