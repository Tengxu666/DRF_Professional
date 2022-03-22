from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):
    """
    自定义异常
    """
    response = exception_handler(exc, context)
    if response is not None:
        response.data['code'] = response.status_code
        try:
            error_msg = response.data['detail']
            del response.data['detail']
        except KeyError:
            return response
        response.data['msg'] = error_msg
        response.status_code = 200
    return response


class ParamsException(APIException):
    """
    serializers自定义错误响应
    """
    def __init__(self, error, code):
        self.detail = error
        self.status_code = code
