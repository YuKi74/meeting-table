from constant.user import password_min_length
from mt.views import MTAuthView, MTView, ResponseData
from user import services

from .serializers import UserSerializerWithoutPassword


class UserView(MTAuthView):

    def get(self, request, id):
        '''
        查看任意用户的个人信息
        '''
        response_data = ResponseData()
        try:
            services.get_information(id, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class UserRegisterView(MTView):

    def post(self, request):
        '''
        用户注册
        '''
        response_data = ResponseData()
        try:
            email = self.check_and_get(request.data, 'email', response_data)
            name = self.check_and_get(request.data, 'name', response_data, 1)
            password = self.check_and_get(
                request.data, 'password', response_data, 6)
            services.register(email, name, password, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class UserLoginView(MTView):

    def post(self, request):
        '''
        用户登录
        '''
        response_data = ResponseData()
        try:
            email = self.check_and_get(request.data, 'email', response_data)
            password = self.check_and_get(
                request.data, 'password', response_data)
            services.login(email, password, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class UserEditView(MTAuthView):

    def patch(self, request):
        '''
        用户修改个人信息
        '''
        response_data = ResponseData()
        user = request.user
        try:
            services.has_data(request.data, response_data)
            self.check_optional_value(request.data, 'name', response_data, 1)
            self.check_optional_value(
                request.data, 'password', response_data, password_min_length)
            services.update_user_information(user, request.data, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def get(self, request):
        '''
        查看用户自己的个人信息
        '''
        response_data = ResponseData()
        response_data.data = UserSerializerWithoutPassword(request.user).data
        return self.respond(response_data)
