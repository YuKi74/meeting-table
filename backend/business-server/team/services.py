from mt.errors import HasTeam
from mt.status import MTStatus
from mt.views import ResponseData
from rest_framework.exceptions import PermissionDenied, ValidationError
from team.models import Application, MeetingRoom, Team
from team.serializers import (ApplicantSerializer, ApplicationSerializer,
                              MeetingRoomSerializer, TeamInformationSerializer,
                              TeamSerializer)
from user.models import User
from user.serializers import UserSerializerWithoutPassword


def has_no_team(user, response_data):
    if user.team:
        response_data.mt_status = MTStatus.FORBIDDEN
        response_data.data = HasTeam.detail
        raise HasTeam()


def has_team(user, response_data):
    if not user.team:
        response_data.mt_status = MTStatus.TEAM_NOT_EXIST
        raise Team.DoesNotExist()


def create_team(name, introduction, creator, response_data):
    team_serializer = TeamSerializer(data={
        'name': name,
        'introduction': introduction,
        'creator': creator.id
    })
    if not team_serializer.is_valid():
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError('输入字段有误')
    team = team_serializer.save()
    creator.team_id = team.id
    creator.save()


def get_team_detail(user, uuid, response_data):
    try:
        team = Team.objects.get(uuid=uuid)
    except Team.DoesNotExist as err:
        response_data.mt_status = MTStatus.TEAM_NOT_EXIST
        raise Team.DoesNotExist from err
    response_data.data = TeamInformationSerializer(team).data
    response_data.data['is_creator'] = team.creator_id == user.id


def is_creator(user, response_data):
    if not user.is_creator():
        response_data.mt_status = MTStatus.FORBIDDEN
        raise PermissionDenied('非创建者无权限进行当前操作')


def has_data(data, response_data):
    if not any(data):
        response_data.mt_status = MTStatus.MISSING_PARAMETER
        raise ValidationError()


def update_team(team, data, response_data):
    team_serializer = TeamSerializer(
        instance=team, data=data, partial=True)
    if not team_serializer.is_valid():
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError()
    team_serializer.save()


def belong_to_team(member_id, team, response_data):
    try:
        member = User.objects.get(id=member_id)
    except User.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前用户不存在'
        raise User.DoesNotExist() from err
    if member.team_id != team.id:
        response_data.mt_status = MTStatus.ERROR_INPUT
        response_data.data = '当前用户不属于本团队'
        raise PermissionDenied()
    return member


def delete_member(member):
    member.team_id = None
    member.save()


def get_team_members(team, response_data):
    members = User.objects.filter(team_id=team.id)
    response_data.data = UserSerializerWithoutPassword(members, many=True).data


def solve_application(application_id, is_admitted, response_data):
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前申请记录不存在'
        raise Application.DoesNotExist() from err
    if application.status != Application.Status.PENDING:
        response_data.mt_status = MTStatus.ERROR_INPUT
        response_data.data = '当前申请记录已处理'
        raise ValidationError()
    user = User.objects.get(id=application.user_id)
    team = Team.objects.get(id=application.team_id)
    if is_admitted == True:
        user.team_id = team.id
        user.save()
        Application.objects.filter(user_id=user.id).update(
            status=Application.Status.DENIED)
        Application.objects.filter(user_id=user.id, team_id=team.id).update(
            status=Application.Status.ACCEPTED)
        application.status = Application.Status.ACCEPTED
    else:
        Application.objects.filter(user_id=user.id, team_id=team.id).update(
            status=Application.Status.DENIED)
        application.status = Application.Status.DENIED
    application.save()


def post_application(user_id, uuid, response_data: ResponseData):
    try:
        team = Team.objects.get(uuid=uuid)
    except Team.DoesNotExist as err:
        response_data.mt_status = MTStatus.TEAM_NOT_EXIST
        raise Team.DoesNotExist() from err
    if Application.objects.filter(user=user_id, team=team.id, status=Application.Status.PENDING):
        response_data.data = "当前用户已提交申请"
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError
    application_serializer = ApplicationSerializer(data={
        'user': user_id,
        'team': team.id
    })
    if application_serializer.is_valid():
        application_serializer.save()


def get_applicants(team_id, response_data):
    applicants = ApplicantSerializer(Application.objects.filter(
        status=Application.Status.PENDING, team_id=team_id), many=True)
    response_data.data = applicants.data


def create_room(user: User, name, response_data: ResponseData):
    room_serializer = MeetingRoomSerializer(data={
        'name': name,
        'creator': user.id,
        'team': user.team_id
    })
    if room_serializer.is_valid():
        room_serializer.save()
    else:
        response_data.mt_status = MTStatus.ERROR_INPUT
        raise ValidationError


def is_room_creator(user: User, room_id, response_data: ResponseData):
    try:
        room = MeetingRoom.objects.get(id=room_id)
    except MeetingRoom.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前会议室不存在'
        raise MeetingRoom.DoesNotExist from err
    if user.id != room.creator_id:
        response_data.mt_status = MTStatus.FORBIDDEN
        response_data.data = '当前用户不是会议室创建人'
        raise PermissionDenied
    return room


def is_room_exist(uuid, response_data: ResponseData):
    try:
        room = MeetingRoom.objects.get(uuid=uuid)
    except MeetingRoom.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前会议室不存在'
        raise MeetingRoom.DoesNotExist from err
    return room


def get_room_information(user: User, room: MeetingRoom, response_data: ResponseData):
    if user.team_id == room.team_id:
        response_data.data = MeetingRoomSerializer(room).data
    else:
        response_data.mt_status = MTStatus.FORBIDDEN
        raise PermissionDenied
