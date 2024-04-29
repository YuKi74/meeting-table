from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request


class ServerAuthentification(BaseAuthentication):
    def authenticate(self, request: Request):
        token = request.META.get('HTTP_TOKEN')
        if not token:
            raise AuthenticationFailed('会议室服务器未携带验证信息', 403)
        elif token != "meeting-table-np":
            raise AuthenticationFailed('会议室服务器验证错误', 403)
