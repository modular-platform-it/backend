# from django.conf import settings
# from django.contrib.auth import login, logout
# from django.shortcuts import redirect
# from drf_spectacular.utils import OpenApiResponse, extend_schema
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from .drf_serializers import (
#     ForbiddenSerializer,
#     LoginResponseSerializer,
#     LoginSerializer,
#     LogoutSerializer,
# )


# @permission_classes([AllowAny])
# @extend_schema(
#     request=LoginSerializer,
#     responses={
#         200: LoginSerializer,
#         400: OpenApiResponse(description="Вы уже авторизованы"),
#     },
#     tags=["Авторизация"],
#     summary="Авторизация пользователя (GET)",
#     methods=["GET"],
# )
# @extend_schema(
#     request=LoginSerializer,
#     responses={
#         200: OpenApiResponse(
#             response=LoginResponseSerializer, description="Успешный вход"
#         ),
#         400: OpenApiResponse(
#             description="Указанные вами адрес электронной почты и/или пароль неверны"
#         ),
#         403: OpenApiResponse(
#             response=ForbiddenSerializer, description="Требуется авторизация"
#         ),
#     },
#     tags=["Авторизация"],
#     summary="Авторизация пользователя (POST)",
#     methods=["POST"],
# )
# @api_view(["GET", "POST"])
# @permission_classes([AllowAny])
# def swagger_login(request):
#     if request.method == "GET":
#         return Response({"description": "Войти."}, status=status.HTTP_200_OK)
#     elif request.method == "POST":
#         if request.user.is_authenticated:
#             return Response(
#                 {"detail": "Вы уже авторизованы."}, status=status.HTTP_400_BAD_REQUEST
#             )
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         if user is not None:
#             login(request, user)
#             return Response({"email": user.email}, status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 {
#                     "detail": "Указанные вами адрес электронной почты и/или пароль неверны."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# @extend_schema(
#     request=LogoutSerializer,
#     responses={
#         200: {"description": "Выйти"},
#         400: OpenApiResponse(description="Сначала авторизуйтесь."),
#     },
#     tags=["Авторизация"],
#     summary="Выход пользователя из системы (GET)",
#     methods=["GET"],
# )
# @extend_schema(
#     request=LogoutSerializer,
#     responses={
#         302: OpenApiResponse(description="Вы вышли"),
#         400: OpenApiResponse(description="Сначала авторизуйтесь."),
#         403: OpenApiResponse(
#             response=ForbiddenSerializer, description="Неверный токен."
#         ),
#     },
#     tags=["Авторизация"],
#     summary="Выход пользователя из системы (POST)",
#     methods=["POST"],
# )
# @api_view(["GET", "POST"])
# def swagger_logout(request):
#     if request.user.is_authenticated:
#         if request.method == "GET":
#             return Response(
#                 {"detail": "Вы уверены, что хотите выйти?"}, status=status.HTTP_200_OK
#             )
#         elif request.method == "POST":
#             logout(request)
#             return redirect("/v1/users/login/")
#     else:
#         return Response(
#             {"detail": "Сначала авторизуйтесь."}, status=status.HTTP_400_BAD_REQUEST
#         )
