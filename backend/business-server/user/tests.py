from constant.user import (default_password, not_exist_user_id,
                           user_test_eamil_one, user_test_eamil_three,
                           user_test_eamil_two)
from django.test import TestCase
from helper.test import create_team, create_user
from mt.status import MTStatus
from mt.views import ResponseData
from rest_framework.exceptions import ValidationError
from user import services

from .models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user(name='username1',
                                 email=user_test_eamil_one, password=default_password)
        self.user2 = create_user(name='username2',
                                 email=user_test_eamil_two, password=default_password)
        self.user3 = create_user(name='username3',
                                 email=user_test_eamil_three, password=default_password)

    def test_get_information(self):
        team1 = create_team('team_name', 'team_introduction', self.user1)
        self.user1.team = team1
        self.user1.save()

        response_data = ResponseData()
        services.get_information(self.user1.id, response_data)
        self.assertEqual(response_data.data['team_uuid'], team1.uuid)

        response_data = ResponseData()
        services.get_information(self.user2.id, response_data)
        self.assertEqual(response_data.data['team_uuid'], None)

        response_data = ResponseData()
        self.assertRaises(User.DoesNotExist,
                          services.get_information, not_exist_user_id, response_data)
        self.assertEqual(response_data.data, '当前用户不存在')
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)

    def test_register(self):
        response_data = ResponseData()
        services.register(name='username5', email='test5@qq.com',
                          password=default_password, response_data=response_data)
        self.assertIn('token', response_data.data.keys())

        response_data = ResponseData()
        self.assertRaises(ValidationError, services.register, 'username5',
                          user_test_eamil_one, default_password, response_data=response_data)
        self.assertEqual(response_data.data, '当前邮箱已被占用')
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)

    def test_login(self):
        response_data = ResponseData()
        self.assertRaises(User.DoesNotExist,
                          services.login, 'wrongemail@qq.com', default_password, response_data)
        self.assertEqual(response_data.data, '当前用户不存在')
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)

        response_data = ResponseData()
        services.login(user_test_eamil_one, default_password, response_data)
        self.assertIn('token', response_data.data.keys())

        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.login, user_test_eamil_one, '12345678', response_data)
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

    def test_get_self_information(self):
        self.team1 = create_team('team_name', 'team_introduction', self.user1)
        self.user1.team = self.team1
        self.user1.save()

        response_data = ResponseData()
        services.get_self_information(self.user1, response_data)
        self.assertEqual(response_data.data['team_uuid'], self.team1.uuid)

        response_data = ResponseData()
        services.get_self_information(self.user2, response_data)
        self.assertEqual(response_data.data['team_uuid'], None)
