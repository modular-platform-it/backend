from api import constants
from rest_framework import status
from rest_framework.exceptions import APIException


class BotIsRunningException(APIException):
    status_code = constants.EXCEPTIONS.get("BOT_IS_RUNNING").get("STATUS_CODE")
    default_detail = constants.EXCEPTIONS.get("BOT_IS_RUNNING").get("DETAIL")
    default_code = constants.EXCEPTIONS.get("BOT_IS_RUNNING").get("DEFAULT_CODE")
