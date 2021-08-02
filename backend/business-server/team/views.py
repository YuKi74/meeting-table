from mt.views import MTAuthView, ResponseData
from team import services
from team.serializers import MeetingRoomSerializer

from .models import MeetingRoom, Team


class TeamView(MTAuthView):
    def post(self, request):
        """
        @api {post} /team/ 创建团队
        @apiName create_team
        @apiGroup Team

        @apiParam {String[1..64]} name 团队名
        @apiParam {String[1..255]} introduction 团队介绍

        @apiParamExample {json} 请求示例
        {
            "name":"干完这单就回家",
            "introduction":"这是团队介绍啊"
        }
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError FORBIDDEN
        """
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
        """
        @api {patch} /team/ 修改团队信息
        @apiName update_team_information
        @apiGroup Team

        @apiParam {String[1..64]} [name] 团队名
        @apiParam {String[1..255]} [introduction] 团队介绍

        @apiError TEAM_NOT_EXIST
        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        """
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
        """
        @api {delete} /team/ 解散团队
        @apiName delete_team
        @apiGroup Team

        @apiError TEAM_NOT_EXIST
        @apiError FORBIDDEN

        """
        response_data = ResponseData()
        user = request.user
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            Team.objects.get(id=user.team_id).delete()
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class TeamMemberView(MTAuthView):

    def get(self, request):
        """
        @api {get} /team/member/ 查看用户所在团队内所有成员
        @apiName get_all_team_members
        @apiGroup Team
        @apiSuccess {String} information 团队内所有成员信息

        @apiError TEAM_NOT_EXIST
        """
        # TODO 看一下返回值类型

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
        """
        @api {delete} /team/member/  团队创建者移出团队内成员
        @apiName delete_team_member
        @apiGroup Team

        @apiParam {Number} member_id 团队成员id

        @apiError TEAM_NOT_EXIST
        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError RECORD_NOT_FOUND
        """
        response_data = ResponseData()
        user = request.user
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            member_id = self.check_and_get(
                request.data, 'member_id', response_data)
            member = services.belong_to_team(
                member_id, user.team, response_data)
            services.delete_member(member)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def post(self, request):
        """
        @api {post} /team/member/ 团队创建者审核申请人
        @apiName process_member_application
        @apiGroup Team

        @apiParam {Number} application_id 申请记录id
        @apiParam {Boolean} is_admitted 申请是否同意

        @apiError TEAM_NOT_EXIST
        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError RECORD_NOT_FOUND
        """
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            services.is_creator(user, response_data)
            application_id = self.check_and_get(
                request.data, 'application_id', response_data)
            is_admitted = bool(self.check_and_get(
                request.data, 'is_admitted', response_data))
            services.solve_application(
                application_id, is_admitted, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class ApplicationView(MTAuthView):

    def post(self, request):
        """
        @api {post} /team/join/ 申请人提交加入团队的申请
        @apiName submit_application
        @apiGroup Team

        @apiParam {String} uuid 申请团队uuid

        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError TEAM_NOT_EXIST
        """
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
        """
        @api {get} /team/join/ 团队创建者获取未处理的申请人名单
        @apiName get_unsolved_applications
        @apiGroup Team

        @apiSuccess {String[]} unsolved_list 未处理的申请人名单

        @apiError FORBIDDEN
        @apiError TEAM_NOT_EXIST
        """
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
        """
        @api {post} /team/quit/ 用户退出团队
        @apiName quit_team
        @apiGroup Team

        @apiError TEAM_NOT_EXIST
        """
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
        """
        @api {get} /team/:uuid 获取团队信息
        @apiName get_team_information
        @apiGroup Team

        @apiSuccess {String[]} team_information 团队信息

        @apiError TEAM_NOT_EXIST
        """

        response_data = ResponseData()
        try:
            services.get_team_detail(uuid, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class MeetingRoomView(MTAuthView):
    def post(self, request):
        """
        @api {post} /room/ 创建会议室
        @apiName create_new_room
        @apiGroup Room

        @apiParam {String[1..64]} name 团队名

        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        """
        user = request.user
        response_data = ResponseData()
        try:
            name = self.check_and_get(request.data, 'name', response_data, 1)
            services.create_room(user, name, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def patch(self, request):
        """
        @api {patch} /room/ 创建人编辑会议室信息
        @apiName update_room_information
        @apiGroup Room

        @apiParam {String[1..64]} name 会议室新名字
        @apiParam {Number} id 会议室id

        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN
        """
        user = request.user
        response_data = ResponseData()
        try:
            id = self.check_and_get(request.data, 'id', response_data)
            name = self.check_and_get(request.data, 'name', response_data, 1)
            room = services.is_room_creator(user, id, response_data)
            room.name = name
            room.save()
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def get(self, request, uuid):
        """
        @api {get} /room/ 获取会议室信息
        @apiName update_room_information
        @apiGroup Room

        @apiParam {String} uuid 会议室uuid

        @apiSuccess {String[]} room_information 会议室信息

        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN
        """
        user = request.user
        response_data = ResponseData()
        try:
            room = services.is_room_exist(uuid, response_data)
            services.get_room_information(user, room, response_data)
        except:
            # TODO log error
            pass

        return self.respond(response_data)

    def delete(self, request):
        """
        @api {delete} /room/ 创建人删除会议室
        @apiName delete_room
        @apiGroup Room

        @apiParam {Number} id 会议室id

        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        """
        user = request.user
        response_data = ResponseData()
        try:
            id = self.check_and_get(request.data, 'id', response_data)
            room = services.is_room_creator(user, id, response_data)
            room.delete()
        except:
            # TODO log error
            pass

        return self.respond(response_data)


class TeamMeetingRoomView(MTAuthView):
    def get(self, request):
        '''
        @api {get} /rooms/ 获取团队内所有会议室信息
        @apiName get_team_rooms_information
        @apiGroup Room

        @apiSuccess {String[]} 会议室信息

        @apiError TEAM_NOT_EXIST
        '''
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            response_data.data = MeetingRoomSerializer(MeetingRoom.objects.filter(
                team_id=user.team_id), many=True).data
        except:
            # TODO log error
            pass

        return self.respond(response_data)
