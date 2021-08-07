from constant.user import password_min_length
from mt.logger import logger
from mt.views import MTAuthView, MTView, ResponseData
from rest_framework.exceptions import ValidationError
from user import services
from user.models import User


class UserView(MTAuthView):

    def get(self, request, user_id):
        """
        @api {get} /user/:user_id/ 用户获取其他用户信息
        @apiExample 请求路径示例
        http://localhost/api/user/1/
        @apiName user_information
        @apiGroup User

        @apiSuccess {String[]} user_information 用户信息
        @apiError RECORD_NOT_FOUND
        """
        response_data = ResponseData()
        try:
            services.get_information(user_id, response_data)
        except (User.DoesNotExist) as e:
            logger.error('url: /user/:user_id/, method: get, error: %s', e)
        return self.respond(response_data)


class UserRegisterView(MTView):

    def post(self, request):
        """
        @api {post} /user/register/ 用户注册
        @apiName user_register
        @apiGroup User

        @apiParam {String} name 用户名
        @apiParam {String} email 用户邮箱
        @apiParam {String} password 用户密码

        @apiParamExample {json} 请求示例
        {
            "name":"gan",
            "email":"test@qq.com",
            "password":"123456"
        }
        @apiSuccess {String} token 后续发请求都要携带
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        """
        response_data = ResponseData()
        try:
            email = self.check_and_get(request.data, 'email', response_data)
            name = self.check_and_get(request.data, 'name', response_data, 1)
            password = self.check_and_get(
                request.data, 'password', response_data, 6)
            services.register(email, name, password, response_data)
        except (ValidationError) as e:
            logger.error('url: /user/register/, method: post, error: %s', e)
        return self.respond(response_data)


class UserLoginView(MTView):

    def post(self, request):
        """
        @api {post} /user/login/ 用户登录
        @apiName user_login
        @apiGroup User

        @apiParam {String} email 用户邮箱
        @apiParam {String} password 用户密码

        @apiParamExample {json} 请求示例
        {
            "email":"test@qq.com",
            "password":"123456"
        }
        @apiSuccess {String} token 后续发请求都要携带
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError RECORD_NOT_FOUND
        """
        response_data = ResponseData()
        try:
            email = self.check_and_get(request.data, 'email', response_data)
            password = self.check_and_get(
                request.data, 'password', response_data)
            services.login(email, password, response_data)
        except (ValidationError, User.DoesNotExist) as e:
            logger.error('url: /user/login/, method: post, error: %s', e)
        return self.respond(response_data)


class UserEditView(MTAuthView):

    def patch(self, request):
        """
        @api {patch} /user/ 用户修改个人信息
        @apiName update_information
        @apiGroup User

        @apiParam {String[1..32]} [name] 用户名
        @apiParam {String[1..128]} [password] 用户密码

        @apiSuccess {String} token 后续发请求都要携带

        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError FORBIDDEN

        """
        response_data = ResponseData()
        user = request.user
        try:
            services.has_data(request.data, response_data)
            self.check_optional_value(request.data, 'name', response_data, 1)
            self.check_optional_value(
                request.data, 'password', response_data, password_min_length)
            services.update_user_information(user, request.data, response_data)
        except (ValidationError, PermissionError) as e:
            logger.error('url: /user/, method: patch, error: %s', e)
        return self.respond(response_data)

    def get(self, request):
        """
        @api {get} /user/ 用户查看个人信息
        @apiHeader token 发送请求时携带token
        @apiName update_information
        @apiGroup User

        @apiSuccess {String} information 用户个人信息
        """
        response_data = ResponseData()
        user = request.user
        services.get_self_information(user, response_data)
        return self.respond(response_data)
