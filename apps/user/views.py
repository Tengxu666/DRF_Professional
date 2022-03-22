from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from apps.user.serializer import UserSignupSerializer, UserSigninSerializer


class UserSignupAPIView(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance

        Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功"}

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


class UserSigninAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        token, _ = Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功", "data": {"token": token.key, "nickname": user.nickname}}

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
