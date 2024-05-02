from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .drf_serializers import LoginSerializer


@extend_schema(
    request=LoginSerializer,
    responses={
        200: LoginSerializer,
    },
    tags=["Авторизация"],
    summary="Авторизация пользователя (GET)",
    methods=["GET"],
)
@extend_schema(
    request=LoginSerializer,
    responses={
        302: {"description": "Успешный вход"},
        400: {
            "description": "Указанные вами адрес электронной почты и/или пароль неверны"
        },
    },
    tags=["Авторизация"],
    summary="Авторизация пользователя (POST)",
    methods=["POST"],
)
@api_view(["GET", "POST"])
def swagger_login(request):
    if request.method == "GET":
        return Response({"description": "Войти."}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if success:
            return Response(
                {"detail": f"Успешный вход под именем {request.user.email}"},
                status=status.HTTP_302_FOUND,
            )
        else:
            return Response(
                {
                    "detail": "Указанные вами адрес электронной почты и/или пароль неверны."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema(
    responses={
        200: {"description": "Выйти"},
    },
    tags=["Авторизация"],
    summary="Выход пользователя из системы (GET)",
    methods=["GET"],
)
@extend_schema(
    responses={
        302: {"description": "Вы вышли."},
    },
    tags=["Авторизация"],
    summary="Выход пользователя из системы (POST)",
    methods=["POST"],
)
@api_view(["GET", "POST"])
def swagger_logout(request):
    if request.method == "GET":
        return Response(
            {"detail": "Вы уверены, что хотите выйти?"}, status=status.HTTP_200_OK
        )
    elif request.method == "POST":
        return Response({"detail": "Вы вышли."}, status=status.HTTP_302_FOUND)
