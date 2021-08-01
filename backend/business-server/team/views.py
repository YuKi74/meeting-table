from mt.views import MTAuthView, ResponseData
from team import services
from .models import Team


class TeamView(MTAuthView):
    def post(self, request):
        '''
        @api {post} /team/ Create a new team
        @apiName create_team
        @apiGroup Team

        @apiParam {String[1..64]} name 团队名
        @apiParam {String[1..255]} introduction 团队介绍

        @api

        '''
        response_data = ResponseData()
        creator = request.user
        try:
            services.has_no_team(creator, response_data)
            name = self.check_and_get(request.data, 'name', response_data)
            introduction = self.check_and_get(
                request.data, 'introduction', response_data)
            services.create_team(name, introduction, creator, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def patch(self, request):
        '''
        修改团队信息，可以传入团队名name，团队介绍introduction（至少传入一个）
        '''
        '''
        @api {patch} /team/ update team information
        @apiName update_team_information
        @apiGroup Team

        @apiParam {String[1..32]} []

        '''
        response_data = ResponseData()
        user = request.user
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            services.has_data(request.data, response_data)
            self.check_optional_value(
                request.data, 'introduction', response_data)
            self.check_optional_value(request.data, 'name', response_data)
            services.update_team(user.team, request.data, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def delete(self, request):
        '''
        解散团队
        '''
        response_data = ResponseData()
        user = request.user
        print('88888')
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            print('lalala')
            Team.objects.get(id=user.team_id).delete()
            print('aaaa')
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class TeamMemberView(MTAuthView):

    def get(self, request):
        '''
        查看团队内所有成员
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            services.get_team_members(user.team, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def delete(self, request):
        '''
        团队创建者移出团队内成员
        '''
        response_data = ResponseData()
        user = request.user
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            member_id = self.check_and_get(
                request.data, 'member_id', response_data)
            services.delete_member(member_id, user.team, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def post(self, request):
        '''
        团队创建者通过修改申请人状态，修改团队内成员，传入申请记录id，是否允许申请is_admitted
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            application_id = self.check_and_get(
                request.data, 'application_id', response_data)
            is_admitted = (self.check_and_get(
                request.data, 'is_admitted', response_data))
            services.solve_application(
                application_id, is_admitted, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class ApplicationView(MTAuthView):

    def post(self, request):
        '''
        申请人提交加入团队的申请，传入团队uuid
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_no_team(user, response_data)
            uuid = self.check_and_get(request.data, 'uuid', response_data)
            services.post_application(user.id, uuid, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def get(self, request):
        '''
        团队创建者获取未处理的申请人名单
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            services.get_applicants(user.team_id, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class TeamMemberQuitView(MTAuthView):

    def post(self, request):
        '''
        用户退出团队
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            user.team_id = None
            user.save()
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class TeamInformationView(MTAuthView):
    def get(self, request, uuid):
        '''
        @api {get} /team/:uuid get team information
        @apiName get_team_information
        @apiGroup Team

        @apiParam {String[1..64]} [name] Team Name
        @apiParam {String[1..255]} [introduction] Team Introduction

        '''

        response_data = ResponseData()
        print('uuid')
        try:
            services.get_team_detail(uuid, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)
