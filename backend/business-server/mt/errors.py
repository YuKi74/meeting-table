from mt.status import MTStatus
from mt.views import MTView, ResponseData
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import exception_handler as drf_exception_handler


class HasTeam(Exception):
    detail = '用户已有所属团队'


def exception_handler(exc, context):
    if isinstance(exc, AuthenticationFailed) and exc.get_codes() == 401:
        response_data = ResponseData(
            data=exc.detail, mt_status=MTStatus.NEED_LOG_IN)
        return MTView.respond(response_data)
    if isinstance(exc, AuthenticationFailed) and exc.get_codes() == 403:
        response_data = ResponseData(
            data=exc.detail, mt_status=MTStatus.SERVER_FORBIDDEN)
        return MTView.respond(response_data)
    response = drf_exception_handler(exc, context)
    return response
