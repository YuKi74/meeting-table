from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


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
