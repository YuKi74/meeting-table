from django.test import TestCase
from rest_framework.exceptions import ValidationError
from mt.status import MTStatus

from .models import User
from user import services
from mt.views import ResponseData
from .serializers import UserSerializerWithoutPassword

from helper.test import create_user
from constant.usertest import not_exist_user_id


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user(name='username1',
                                 email='test1@qq.com', password='123456')
        self.user2 = create_user(name='username2',
                                 email='test2@qq.com', password='123456')
        self.user3 = create_user(name='username3',
                                 email='test3@qq.com', password='123456')

    def test_get_information(self):
        response_data = ResponseData()
        services.get_information(self.user1.id, response_data)
        self.assertEqual(response_data.data,
                         UserSerializerWithoutPassword(self.user1).data)

        response_data = ResponseData()
        self.assertRaises(User.DoesNotExist,
                          services.get_information, not_exist_user_id, response_data)
        self.assertEqual(response_data.data, '当前用户不存在')
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)

    def test_register(self):
        response_data = ResponseData()
        services.register(name='username5', email='test5@qq.com',
                          password='123456', response_data=response_data)
        self.assertIn('token', response_data.data.keys())

        response_data = ResponseData()
        self.assertRaises(ValidationError, services.register, 'username5',
                          'test1@qq.com', '123456', response_data=response_data)
        self.assertEqual(response_data.data, '当前邮箱已被占用')
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)

    def test_login(self):
        response_data = ResponseData()
        self.assertRaises(User.DoesNotExist,
                          services.login, 'wrongemail@qq.com', '123456', response_data)
        self.assertEqual(response_data.data, '当前用户不存在')
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)

        response_data = ResponseData()
        services.login('test1@qq.com', '123456', response_data)
        self.assertIn('token', response_data.data.keys())

        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.login, 'test1@qq.com', '12345678', response_data)
        self.assertEqual(response_data.data, '密码输入错误')
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)

    def test_has_data(self):
        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.has_data, {}, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.MISSING_PARAMETER)

        response_data = ResponseData()
        services.has_data({'name': 'newname'}, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

    def test_update_user_information(self):
        response_data = ResponseData()
        data = {'email': 'test@qq.com'}
        self.assertRaises(PermissionError,
                          services.update_user_information, self.user1, data, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.FORBIDDEN)
        self.assertEqual(response_data.data, '邮箱不可更改')

        response_data = ResponseData()
        data = {'name': 'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongnamemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm'}
        self.assertRaises(ValidationError,
                          services.update_user_information, self.user1, data, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)

        response_data = ResponseData()
        data = {'name': 'newname'}
        services.update_user_information(self.user1, data, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        response_data = ResponseData()
        data = {'password': 'newpassword'}
        services.update_user_information(self.user1, data, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        response_data = ResponseData()
        data = {'password': 'newpassword',
                'name': 'newname'}
        services.update_user_information(self.user1, data, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)
