from rest_framework import status
from rest_framework.exceptions import APIException


class BotIsRunningException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Сначала остановите бота"
    default_code = "stop required"
