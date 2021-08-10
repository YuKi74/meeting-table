from constant.mt import (default_email, response_data_not_in_regular_form,
                         test_length_limitation)
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .views import MTStatus, MTView, ResponseData


class MTViewTestCase(TestCase):

    def test_respond(self):
        response = MTView.respond(None)
        self.assertEqual(response.data['data'],
                         MTStatus.INTERNAL_SERVER_ERROR.message)

        response = MTView.respond(response_data_not_in_regular_form)
        self.assertEqual(response.data['data'],
                         MTStatus.INTERNAL_SERVER_ERROR.message
                         )

        response_data = ResponseData()
        response_data.mt_status = None
        response = MTView.respond(response_data)
        self.assertEqual(response.data['data'],
                         MTStatus.INTERNAL_SERVER_ERROR.message)

        response_data = ResponseData('response_data.data is not None')
        response = MTView.respond(response_data)
        self.assertEqual(response.data['data'],
                         'response_data.data is not None')

        response_data = ResponseData()
        response = MTView.respond(response_data)
        self.assertEqual(response.data['data'],
                         MTStatus.OK.message)

    def test_check_and_get(self):
        data = {'email': default_email}
        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          MTView.check_and_get,
                          data, 'name',
                          response_data
                          )
        self.assertEqual(response_data.data, '请求缺少字段："name"')

        data = {'name': ''}
        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          MTView.check_and_get,
                          data, 'name',
                          response_data,
                          test_length_limitation
                          )
        self.assertEqual(response_data.data, '输入值"name"长度不可小于%d位' %
                         test_length_limitation)

        data = {'email': default_email}
        response_data = ResponseData()
        value = MTView.check_and_get(data, 'email', response_data)
        self.assertEqual(value, default_email)

    def test_check_optional_value(self):
        data = {'name': ''}
        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          MTView.check_optional_value,
                          data, 'name',
                          response_data,
                          test_length_limitation
                          )
        self.assertEqual(response_data.data, '输入值"name"长度不可小于%d位' %
                         test_length_limitation)

        data = {}
        response_data = ResponseData()
        MTView.check_optional_value(data, 'name', response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        data = {}
        response_data = ResponseData()
        MTView.check_optional_value(
            data, 'name', response_data, test_length_limitation)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        data = {'name': ''}
        response_data = ResponseData()
        MTView.check_optional_value(data, 'name', response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        data = {'name': 'testname'}
        response_data = ResponseData()
        MTView.check_optional_value(
            data, 'name', response_data, test_length_limitation)
        self.assertEqual(response_data.mt_status, MTStatus.OK)
