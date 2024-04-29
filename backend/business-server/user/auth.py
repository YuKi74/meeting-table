from mt.redis import redis
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from .models import User


class Authentication(BaseAuthentication):
    def authenticate(self, request: Request):
        try:
            token = request.META.get('HTTP_TOKEN')
            if not token:
                raise AuthenticationFailed('未携带token或未登录', 401)
            user_id = redis.get(token)
            if user_id is None:
                raise AuthenticationFailed('token过期或未登录', 401)
            else:
                user = User.objects.get(id=user_id)
                return user, token
        except User.DoesNotExist as err:
            raise AuthenticationFailed('当前用户不存在', 401) from err
