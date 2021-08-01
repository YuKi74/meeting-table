from django.urls.base import is_valid_path
from mt.errors import HasTeam
from mt.status import MTStatus
from rest_framework.exceptions import PermissionDenied, ValidationError
from team.models import Application, Team
from team.serializers import (ApplicantSerializer, ApplicationSerializer,
                              TeamInformationSerializer, TeamSerializer)
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


def get_team_detail(uuid, response_data):
    try:
        team = Team.objects.get(uuid=uuid)
    except Team.DoesNotExist as err:
        response_data.mt_status = MTStatus.TEAM_NOT_EXIST
        print(123123123)
        raise Team.DoesNotExist from err
    print(7897897879789)
    response_data.data = TeamInformationSerializer(team).data


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


def delete_member(member_id, team, response_data):
    try:
        member = User.objects.get(id=member_id)
    except User.DoesNotExist as err:
        response_data.mt_status = MTStatus.RECORD_NOT_FOUND
        response_data.data = '当前用户不存在'
        raise User.DoesNotExist() from err
    if member.team_id == team.id:
        member.team_id = None
        member.save()
    else:
        response_data.mt_status = MTStatus.ERROR_INPUT
        response_data.data = '当前用户不属于本团队'
        raise PermissionDenied()


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
    print(is_admitted)
    print(type(is_admitted))
    if is_admitted == "True":
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


def post_application(user_id, uuid, response_data):
    try:
        team = Team.objects.get(uuid=uuid)
    except Team.DoesNotExist as err:
        response_data.mt_status = MTStatus.TEAM_NOT_EXIST
        raise Team.DoesNotExist() from err
    application_serializer = ApplicationSerializer(data={
        'user': user_id,
        'team': team.id
    })
    print('111')
    if(application_serializer.is_valid()):
        applicant = application_serializer.save()
        print(applicant.id)


def get_applicants(team_id, response_data):
    applicants = ApplicantSerializer(Application.objects.filter(
        status=Application.Status.PENDING, team_id=team_id), many=True)
    response_data.data = applicants.data
