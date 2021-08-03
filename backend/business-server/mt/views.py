"""
自定义APIView
"""
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from user.auth import Authentication

from .status import MTStatus, Status


class ResponseData:
    def __init__(self, data=None, mt_status=MTStatus.OK):
        self.data = data
        self.mt_status = mt_status


class MTView(APIView):
    """
    自定义APIView，封装响应函数与字段验证。
    """

    @staticmethod
    def respond(response_data=None):
        if not response_data \
                or not isinstance(response_data, ResponseData) \
                or not isinstance(response_data.mt_status, Status):
            response_data = ResponseData(
                mt_status=MTStatus.INTERNAL_SERVER_ERROR)
        if response_data.data is None:
            response_data.data = response_data.mt_status.message
        return Response(data={
            'status': response_data.mt_status.mt_code,
            'data': response_data.data,
        }, status=response_data.mt_status.status_code)

    @staticmethod
    def check_and_get(data: Request.DATA, field: str, response_data: ResponseData, length_limitation=None):
        """
        检查并返回请求的字段
        """
        value = data.get(field)
        if value is None:
            response_data.mt_status = MTStatus.MISSING_PARAMETER
            response_data.data = '请求缺少字段："%s"' % field
            raise ValidationError()
        if length_limitation is not None and len(value) < length_limitation:
            response_data.mt_status = MTStatus.ERROR_INPUT
            response_data.data = '输入值"%s"长度不可小于%d位' % (
                field, length_limitation)
            raise ValidationError()
        return value

    @staticmethod
    def check_optional_value(data: Request.DATA, field: str, response_data: ResponseData, length_limitation=None):
        """
        检查并返回部分更新的字段
        """
        value = data.get(field)
        if value is not None \
                and length_limitation is not None \
                and len(value) < length_limitation:
            response_data.mt_status = MTStatus.ERROR_INPUT
            response_data.data = '输入值"%s"长度不可小于%d位' % (
                field, length_limitation)
            raise ValidationError()


class MTAuthView(MTView):
    """
    带身份验证的MTView
    """
    authentication_classes = [Authentication]
