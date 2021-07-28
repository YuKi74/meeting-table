from rest_framework.response import Response
from rest_framework.views import APIView
from mt.redis import redis, token_expire, genetate_token
from user.models import User
from .serializers import UserSerializer, UserSerializerWithoutPassword
from rest_framework import status
from mt.views import MTAuthView, MTView
from mt.status import MTStatus
from rest_framework.exceptions import ValidationError
from constant.user import password_min_length


class UserView(MTAuthView):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            user_serializer = UserSerializerWithoutPassword(user)
            return self.success(user_serializer.data)
        except User.DoesNotExist:
            return self.fail('用户不存在', MTStatus.RECORD_NOT_FOUND)


class UserRegisterView(MTView):
    def post(self, request):
        try:
            email = self.check_and_get(request.data, 'email')
            name = self.check_and_get(request.data, 'name')
            password = self.check_and_get(request.data, 'password')
        except ValidationError as err:
            return self.fail(err.detail, MTStatus.MISSING_PARAMETER)

        if len(str(password)) < password_min_length:
            return self.fail('密码不能短于'+password_min_length+'位', MTStatus.ERROR_INPUT)
        user = User(email=email, name=name, password=password)
        user.set_password(password)
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user.save()
            token = genetate_token(user.id)
            return self.success({'token': token})
        return self.fail('当前邮箱已被占用')


class UserLoginView(MTView):
    def post(self, request):
        try:
            email = self.check_and_get(request.data, 'email')
            password = self.check_and_get(request.data, 'password')
            user = User.objects.get(email=email)
            if user.check_password(password):
                token = genetate_token(user.id)
                return self.success({'token': token})
            else:
                return self.fail('密码输入错误', MTStatus.ERROR_INPUT)
        except User.DoesNotExist:
            return self.fail('用户不存在', MTStatus.RECORD_NOT_FOUND)
        except ValidationError as err:
            return self.fail(err.detail, MTStatus.MISSING_PARAMETER)


class UserEditView(MTAuthView):
    def patch(self, request):
        email = request.data.get('email')
        if email is not None:
            return self.fail('邮箱不可更改', MTStatus.ERROR_INPUT)
        if not any(request.data):
            return self.fail('请输入修改内容', MTStatus.MISSING_PARAMETER)
        name = request.data.get('name')
        password = request.data.get('password')
        if name is not None and not name:
            return self.fail('用户名不能为空', MTStatus.ERROR_INPUT)
        if password is not None and len(str(password)) < password_min_length:
            return self.fail('密码不能短于'+password_min_length+'位', MTStatus.ERROR_INPUT)
        user = request.user
        user_serializer = UserSerializer(
            instance=user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return self.success()
        else:
            return self.fail()
