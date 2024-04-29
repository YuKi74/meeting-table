from mt.errors import HasTeam
from mt.logger import logger
from mt.views import MTAuthView, MTView, ResponseData
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.request import Request
from team import services
from team.serializers import MeetingRoomFileSerializer, MeetingRoomSerializer
from user.models import User

from .models import Application, MeetingRoom, MeetingRoomFiles, Team


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
        except (HasTeam, ValidationError) as e:
            logger.error('url: /team/, method: post, error: %s', e)
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
        except (Team.DoesNotExist, PermissionDenied, ValidationError) as e:
            logger.error('url: /team/, method: patch, error: %s', e)
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
        except (Team.DoesNotExist, PermissionDenied) as e:
            logger.error('url: /team/, method: delete, error: %s', e)
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

        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            services.get_team_members(user.team, response_data)
        except (Team.DoesNotExist) as e:
            logger.error('url: /team/member/, method: get, error: %s', e)
        return self.respond(response_data)

    def delete(self, request, member_id):
        """
        @api {delete} /team/member/：member_id/  团队创建者移出团队内成员
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
            member = services.belong_to_team(
                member_id, user.team, response_data)
            services.delete_member(member)
        except (Team.DoesNotExist, PermissionDenied, User.DoesNotExist) as e:
            logger.error(
                'url: /team/member/：member_id/, method: delete, error: %s', e)
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
        except (Team.DoesNotExist, PermissionDenied, Application.DoesNotExist, ValidationError) as e:
            logger.error(
                'url: /team/member/, method: post, error: %s', e)
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
        except (HasTeam, Team.DoesNotExist, ValidationError) as e:
            logger.error('url: /team/join/, method: post, error: %s', e)
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
        except (Team.DoesNotExist, PermissionDenied) as e:
            logger.error('url: /team/join/, method: get, error: %s', e)
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
        except (Team.DoesNotExist) as e:
            logger.error('url: /team/quit/, method: post, error: %s', e)
        return self.respond(response_data)


class TeamInformationView(MTView):
    def get(self, request: Request, uuid):
        """
        @api {get} /team/:uuid/ 获取团队信息
        @apiName get_team_information
        @apiGroup Team

        @apiSuccess {String[]} team_information 团队信息

        @apiError TEAM_NOT_EXIST
        @apiError ERROR_INPUT
        """

        response_data = ResponseData()
        try:
            token = request.META.get('HTTP_TOKEN')
            user = services.get_user_by_token(token)
            services.get_team_detail(user, uuid, response_data)
        except (Team.DoesNotExist) as e:
            logger.error('url: /team/:uuid/, method: get, error: %s', e)
        return self.respond(response_data)


class MeetingRoomView(MTAuthView):
    def post(self, request):
        """
        @api {post} /team/room/ 创建会议室
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
        except (ValidationError) as e:
            logger.error('url: /team/room/, method: post, error: %s', e)
        return self.respond(response_data)

    def patch(self, request):
        """
        @api {patch} /team/room/ 创建人编辑会议室信息
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
            room_id = self.check_and_get(request.data, 'id', response_data)
            name = self.check_and_get(request.data, 'name', response_data, 1)
            room = services.is_room_creator(user, room_id, response_data)
            room.name = name
            room.save()
        except (ValidationError, MeetingRoom.DoesNotExist, PermissionDenied) as e:
            logger.error('url: /team/room/, method: patch, error: %s', e)
        return self.respond(response_data)

    def get(self, request, uuid):
        """
        @api {get} /team/room/:uuid/ 获取会议室信息
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
            room = services.check_room_by_uuid(uuid, response_data)
            services.get_room_information(user, room, response_data)
        except (MeetingRoom.DoesNotExist, PermissionDenied) as e:
            logger.error('url: /team/room/:uuid/, method: get, error: %s', e)
        return self.respond(response_data)

    def delete(self, request, room_id):
        """
        @api {delete} /team/room/:room_id/ 创建人删除会议室
        @apiName delete_room
        @apiGroup Room

        @apiParam {Number} room_id 会议室id

        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN
        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        """
        user = request.user
        response_data = ResponseData()
        try:
            room = services.is_room_creator(user, room_id, response_data)
            room.delete()
        except (MeetingRoom.DoesNotExist, PermissionDenied) as e:
            logger.error(
                'url: /team/room/:room_id/, method: delete, error: %s', e)
        return self.respond(response_data)


class TeamMeetingRoomView(MTAuthView):
    def get(self, request):
        """
        @api {get} /team/rooms/ 获取团队内所有会议室信息
        @apiName get_team_rooms_information
        @apiGroup Room

        @apiSuccess {String} information 会议室信息

        @apiError TEAM_NOT_EXIST
        """
        user = request.user
        response_data = ResponseData()
        try:
            services.has_team(user, response_data)
            response_data.data = MeetingRoomSerializer(MeetingRoom.objects.filter(
                team_id=user.team_id), many=True).data
        except (Team.DoesNotExist) as e:
            logger.error(
                'url: /team/rooms/, method: get, error: %s', e)
        return self.respond(response_data)


class FileView(MTAuthView):
    def post(self, request, uuid):
        """
        @api {post} /team/file/:uuid/ 在会议室内上传文件
        @apiName upload_file
        @apiGroup Room

        @apiParam {Number} uuid 会议室uuid

        @apiError RECORD_NOT_FOUND
        @apiError MISSING_PARAMETER
        @apiError FORBIDDEN
        @apiError ERROR_INPUT
        """
        response_data = ResponseData()
        try:
            room = services.check_room_by_uuid(uuid, response_data)
            file = services.is_file_uploaded(request, response_data)
            services.upload_file(room.id, file, file.name, response_data)
        except (MeetingRoom.DoesNotExist, ValidationError, PermissionDenied) as e:
            logger.error(
                'url: /team/file/:uuid/, method: post, error: %s', e)
        return self.respond(response_data)

    def get(self, request, uuid):
        """
        @api {get} /team/file/:uuid/ 查看会议室内所有文件
        @apiName get_room_files
        @apiGroup File

        @apiSuccess {String} data 所有会议室内文件信息

        @apiError RECORD_NOT_FOUND
        """
        response_data = ResponseData()
        try:
            room = services.check_room_by_uuid(uuid, response_data)
            response_data.data = MeetingRoomFileSerializer(
                MeetingRoomFiles.objects.filter(meetingRoom=room), many=True).data
        except (MeetingRoom.DoesNotExist) as e:
            logger.error(
                'url: /team/file/:uuid/, method: get, error: %s', e)
        return self.respond(response_data)


class FileTransferView(MTAuthView):
    def delete(self, request, record_id):
        """
        @api {delete} /team/file/:record_id/ 会议室服务器删除会议室内文件
        @apiName delete_file
        @apiGroup File

        @apiParam {Number} record_id 会议室文件记录id

        @apiError RECORD_NOT_FOUND
        """
        response_data = ResponseData()
        try:
            file_record = services.is_file_record_exist(
                record_id, response_data)
            file = file_record.files
            if MeetingRoomFiles.objects.filter(files=file).count() == 1:
                file.delete(save=True)
            file_record.delete()
        except (MeetingRoomFiles.DoesNotExist) as e:
            logger.error(
                'url: /team/file/:record_id/, method: delete, error: %s', e)
        return self.respond(response_data)

    def post(self, request):
        """
        @api {post} /team/file/ 从某个会议室转移文件到另一个会议室
        @apiName transfer_file
        @apiGroup File

        @apiParam {Number} room_id 会议室id
        @apiParam {Number} record_id 文件记录id

        @apiError MISSING_PARAMETER
        @apiError ERROR_INPUT
        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN
        """
        response_data = ResponseData()
        try:
            room_id = self.check_and_get(
                request.data, 'room_id', response_data)
            services.check_room_by_id(room_id, response_data)
            record_id = self.check_and_get(
                request.data, 'record_id', response_data)
            record = services.is_file_record_exist(
                record_id, response_data)
            services.file_transfer(room_id, record, response_data)
        except (ValidationError, MeetingRoom.DoesNotExist, PermissionDenied, MeetingRoomFiles.DoesNotExist) as e:
            logger.error(
                'url: /team/file/, method: post, error: %s', e)
        return self.respond(response_data)


class VideoTokenView(MTAuthView):
    def get(self, request, room_uuid):
        """
        @api {get} /team/video_token/:uuid 获取视频通话Token
        @apiName video_token
        @apiGroup video

        @apiError TEAM_NOT_EXIST
        @apiError RECORD_NOT_FOUND
        @apiError FORBIDDEN

        @apiSuccess {String} token 视频通话Token
        """
        response_data = ResponseData()
        user = request.user
        try:
            services.has_team(user, response_data)
            room = services.check_room_by_uuid(room_uuid, response_data)
            services.team_has_room(user.team.id, room, response_data)
            services.generate_video_token(user.id, room_uuid, response_data)
        except(Team.DoesNotExist, MeetingRoom.DoesNotExist, PermissionDenied) as e:
            logger.error(
                'url: /team/video_token/:uuid/, method: get, error: %s', e
            )

        return self.respond(response_data)
