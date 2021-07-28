"""
自定义APIView
"""
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .status import MTStatus
from user.auth import Authentication


class MTView(APIView):
    """
    自定义APIView，封装响应函数与字段验证。
    """

    @staticmethod
    def success(data=None):
        """
        请求成功时调用
        """
        if data is None:
            data = MTStatus.OK.message

        mt_data = {
            'status': MTStatus.OK.mt_code,
            'data': data,
        }
        return Response(data=mt_data, status=MTStatus.OK.status_code)

    @staticmethod
    def fail(data=None, mt_status=MTStatus.ERROR_INPUT):
        """
        请求失败时调用
        """
        if data is None:
            data = mt_status.message

        mt_data = {
            'status': mt_status.mt_code,
            'data': data,
        }
        return Response(data=mt_data, status=mt_status.status_code)

    @staticmethod
    def check_and_get(data: Request.DATA, field: str):
        """
        检查并返回请求的字段
        """
        value = data.get(field)
        if value is None:
            raise ValidationError('请求缺少字段："%s"' % field)
        return value


class MTAuthView(MTView):
    """
    带身份验证的MTView
    """
    authentication_classes = [Authentication]
