from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                                   HTTP_500_INTERNAL_SERVER_ERROR)


class Status:
    def __init__(self, code: int, message: str, status_code: int):
        self.mt_code = code
        self.message = message
        self.status_code = status_code


class MTStatus:
    OK = Status(1, 'OK', HTTP_200_OK)
    NEED_LOG_IN = Status(2, '未提供token或token已失效', HTTP_401_UNAUTHORIZED)
    MISSING_PARAMETER = Status(3, '请求参数不完整', HTTP_400_BAD_REQUEST)
    RECORD_NOT_FOUND = Status(4, '查找的数据不存在', HTTP_400_BAD_REQUEST)
    ERROR_INPUT = Status(5, '输入数据有误', HTTP_400_BAD_REQUEST)
    INTERNAL_SERVER_ERROR = Status(
        6, '服务器内部错误', HTTP_500_INTERNAL_SERVER_ERROR)

    # 用户请求数据部分
    FORBIDDEN = Status(100, '当前用户没有权限', HTTP_403_FORBIDDEN)
    TEAM_NOT_EXIST = Status(101, '当前团队不存在', HTTP_400_BAD_REQUEST)

    # 会议室服务器部分
    SERVER_FORBIDDEN = Status(102, '会议室服务器未通过验证', HTTP_403_FORBIDDEN)
