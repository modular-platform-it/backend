from rest_framework import status

EXCEPTIONS = {
    "BOT_IS_RUNNING": {
        "STATUS_CODE": status.HTTP_400_BAD_REQUEST,
        "DETAIL": "Сначала остановите бота",
        "DEFAULT_CODE": "stop required",
    }
}
