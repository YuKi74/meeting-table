from mt.redis import genetate_token
from mt.status import MTStatus
from mt.views import ResponseData
from rest_framework.exceptions import ValidationError
from team.models import Team

from .models import User
from .serializers import UserSerializer, UserSerializerWithoutPassword


def get_information(id, response_data):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前用户不存在'
        raise User.DoesNotExist() from err
    response_data.data = UserSerializerWithoutPassword(user).data
    response_data.data['team_uuid'] = user.team.uuid if user.team else None


def register(email, name, password, response_data: ResponseData):
    if User.objects.filter(email=email):
        response_data.mt_status = MTStatus.ERROR_INPUT
        response_data.data = '当前邮箱已被占用'
        raise ValidationError()
    user_serializer = UserSerializer(data={
        'name': name,
        'email': email,
        'password': password
    })
    if user_serializer.is_valid():
        user = User(email=email, name=name, password=password)
        user.set_password(password)
        user.save()
        token = genetate_token(user.id)
        response_data.mt_status = MTStatus.OK
        response_data.data = {'token': token}
    else:
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError()


def login(email, password, response_data):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前用户不存在'
        raise User.DoesNotExist from err
    if user.check_password(password):
        token = genetate_token(user.id)
        response_data.data = {'token': token}
    else:
        response_data.mt_status = MTStatus.ERROR_INPUT
        response_data.data = '密码输入错误'
        raise ValidationError()


def has_data(data, response_data):
    if not any(data):
        response_data.mt_status = MTStatus.MISSING_PARAMETER
        raise ValidationError()


def update_user_information(user: User, data, response_data: ResponseData):
    if data.get('email') is not None:
        response_data.mt_status = MTStatus.FORBIDDEN
        response_data.data = '邮箱不可更改'
        raise PermissionError()
    updated_user_serializer = UserSerializer(
        instance=user, data=data, partial=True)
    if updated_user_serializer.is_valid():
        updated_user = updated_user_serializer.save()
        password = data.get('password')
        if password is not None:
            updated_user.set_password(password)
            updated_user.save()
    else:
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError()


def get_self_information(user, response_data):
    response_data.data = UserSerializerWithoutPassword(user).data
    response_data.data['team_uuid'] = user.team.uuid if user.team else None
