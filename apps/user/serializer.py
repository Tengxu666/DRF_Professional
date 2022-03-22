import re
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.user.models import User
from utils.exception import ParamsException


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'username',
            'password',
            'confirm_password',
            'sex',
            'code'
        ]

    default_error_messages = {
        'code_error': '验证码不正确',
        'password_error': '两次密码输入不正确',
        "username_error": '手机号码格式不正确',
    }

    def validate(self, attrs):
        if not re.match(r'^1[3-9]\d{9}$', attrs['username']):
            raise ParamsException(self.error_messages['username_error'], 422)
        if attrs.get('code') != '123':
            raise ParamsException(self.error_messages['code_error'], 422)
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ParamsException(self.error_messages['password_error'], 422)
        del attrs['confirm_password']
        del attrs['code']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': '用户已被禁用',
        'invalid_credentials': '账号或密码无效'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise ParamsException(self.error_messages['inactive_account'], 404)
            return attrs
        else:
            raise ParamsException(self.error_messages['invalid_credentials'], 404)
