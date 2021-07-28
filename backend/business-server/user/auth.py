from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from mt.redis import redis
from .models import User


class Authentication(BaseAuthentication):
    def authenticate(self, request: Request):
        try:
            token = request.META.get('HTTP_TOKEN')
            if not token:
                raise AuthenticationFailed('未携带token或未登录')
            id = redis.get(token)
            if id is None:
                raise AuthenticationFailed('token过期或未登录')
            else:
                user = User.objects.get(id=id)
                return user, token
        except User.DoesNotExist:
            raise AuthenticationFailed('当前用户不存在')
