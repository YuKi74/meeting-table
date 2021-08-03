from constant.team import (not_exist_application_id, not_exist_room_id,
                           not_exist_room_uuid, not_exist_team_uuid,
                           not_exist_user_id)
from django.test import TestCase
from helper.test import (create_application, create_room, create_team,
                         create_user)
from mt.errors import HasTeam
from mt.status import MTStatus
from mt.views import ResponseData
from rest_framework.exceptions import PermissionDenied, ValidationError
from team import services
from team.models import MeetingRoom, Team
from team.serializers import MeetingRoomSerializer
from user.models import User
from user.serializers import UserSerializerWithoutPassword

from .models import Application, Team
from .serializers import ApplicantSerializer, TeamInformationSerializer


class TeamTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user(
            name='username1',
            email='test1@qq.com',
            password='123456'
        )
        self.team1 = create_team(
            name='teamname1',
            introduction='test',
            creator=self.user1
        )
        self.user1.team = self.team1
        self.user1.save()

        self.user2 = create_user(
            name='username2',
            email='test2@qq.com',
            password='123456'
        )

    def test_has_no_team(self):
        response_data = ResponseData()
        self.assertRaises(HasTeam, services.has_no_team,
                          self.user1, response_data)

        response_data = ResponseData()
        services.has_no_team(self.user2, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

    def test_create_team(self):
        self.user3 = create_user(
            name='username3',
            email='test3@qq.com',
            password='123456'
        )

        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.create_team,
                          name='toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongnamemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                          introduction='test',
                          creator=self.user3,
                          response_data=response_data)

        # response_data = ResponseData()
        # # TODO 检查数据库字段限制
        # self.assertRaises(ValidationError,
        #                   services.create_team,
        #                   name='teamname2',
        #                   introduction='tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongintroductionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
        #                   creator=self.user3,
        #                   response_data=response_data)

        response_data = ResponseData()
        services.create_team(
            name='teamname3',
            introduction='test',
            creator=self.user3,
            response_data=response_data)
        self.assertNotEqual(self.user3.team, None)

    def test_update_team(self):
        self.team2 = create_team(
            name='teamname2',
            introduction='test',
            creator=self.user2
        )

        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.update_team,
                          self.team2,
                          {'name': 'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongnamemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm'},
                          response_data=response_data)

        # response_data = ResponseData()
        # self.assertRaises(ValidationError,
        #                   services.update_team,
        #                   self.team2,
        #                   {'introduction': 'tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongintroductionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn'},
        #                   response_data=response_data)

        response_data = ResponseData()
        services.update_team(
            self.team2,
            {'name': 'teamname3',
             'introduction': 'test'},
            response_data=response_data)
        self.assertEqual(self.team2.name, 'teamname3')
        self.assertEqual(self.team2.introduction, 'test')

        response_data = ResponseData()
        services.update_team(
            self.team2,
            {'name': 'teamname4'},
            response_data=response_data)
        self.assertEqual(self.team2.name, 'teamname4')

        response_data = ResponseData()
        services.update_team(
            self.team2,
            {'introduction': 'test2'},
            response_data=response_data)
        self.assertEqual(self.team2.introduction, 'test2')


class ApplicationProcessTestCase(TestCase):
    def setUp(self):
        self.creator1 = create_user(
            name='username1',
            email='test1@qq.com',
            password='123456'
        )
        self.team1 = create_team(
            name='teamname1',
            introduction='test',
            creator=self.creator1
        )
        self.creator1.team = self.team1
        self.creator1.save()
        self.creator2 = create_user(
            name='username2',
            email='test2@qq.com',
            password='123456'
        )
        self.team2 = create_team(
            name='teamname2',
            introduction='test',
            creator=self.creator2
        )
        self.creator2.team = self.team2
        self.creator2.save()
        self.user1 = create_user(
            name='username3',
            email='test3@qq.com',
            password='123456'
        )
        self.user2 = create_user(
            name='username4',
            email='test4@qq.com',
            password='123456'
        )

    def test_solve_application(self):
        self.application1 = create_application(
            user=self.user1,
            team=self.team1
        )
        self.application2 = create_application(
            user=self.user1,
            team=self.team2
        )
        self.application3 = create_application(
            user=self.user2,
            team=self.team1
        )
        self.application4 = create_application(
            user=self.user2,
            team=self.team2
        )

        response_data = ResponseData()
        self.assertRaises(Application.DoesNotExist,
                          services.solve_application,
                          not_exist_application_id,
                          True,
                          response_data)
        self.assertEqual(response_data.data, '当前申请记录不存在')

        response_data = ResponseData()
        self.application1.status = Application.Status.ACCEPTED
        self.application1.save()
        self.assertRaises(ValidationError,
                          services.solve_application,
                          self.application1.id,
                          True,
                          response_data)
        self.assertEqual(response_data.data, '当前申请记录已处理')
        self.application1.status = Application.Status.PENDING
        self.application1.save()

        response_data = ResponseData()
        services.solve_application(self.application3.id,
                                   False,
                                   response_data)
        self.assertEqual(Application.objects.get(id=self.application3.id).status,
                         Application.Status.DENIED)
        self.assertEqual(Application.objects.get(id=self.application4.id).status,
                         Application.Status.PENDING)
        self.application3.status = Application.Status.PENDING
        self.application1.save()

        response_data = ResponseData()
        services.solve_application(self.application1.id,
                                   True,
                                   response_data)
        self.assertEqual(Application.objects.get(id=self.application1.id).status,
                         Application.Status.ACCEPTED)
        self.assertEqual(Application.objects.get(id=self.application2.id).status,
                         Application.Status.DENIED)
        self.application1.status = Application.Status.PENDING
        self.application1.save()
        self.application2.status = Application.Status.PENDING
        self.application2.save()

    def test_post_application(self):
        response_data = ResponseData()
        self.assertRaises(
            Team.DoesNotExist,
            services.post_application,
            self.user1.id,
            not_exist_team_uuid,
            response_data)
        self.assertEqual(response_data.mt_status, MTStatus.TEAM_NOT_EXIST)

        response_data = ResponseData()
        services.post_application(self.user1, self.team1.uuid, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

    def test_get_applicants(self):
        response_data = ResponseData()
        services.get_applicants(self.team1.id, response_data)
        self.assertEqual(response_data.data, ApplicantSerializer(Application.objects.filter(
            status=Application.Status.PENDING, team_id=self.team1.id), many=True).data)

    def test_get_team_detail(self):
        response_data = ResponseData()
        self.assertRaises(
            Team.DoesNotExist,
            services.get_team_detail,
            self.creator1,
            not_exist_team_uuid,
            response_data)
        self.assertEqual(response_data.mt_status, MTStatus.TEAM_NOT_EXIST)

        response_data = ResponseData()
        services.get_team_detail(self.creator1, self.team1.uuid, response_data)
        self.assertEqual(response_data.data['is_creator'], True)

        response_data = ResponseData()
        services.get_team_detail(self.user1, self.team1.uuid, response_data)
        self.assertEqual(response_data.data['is_creator'], False)


class MeetingRoomTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user(
            name='username1',
            email='test1@qq.com',
            password='123456')
        self.user2 = create_user(
            name='username2',
            email='test2@qq.com',
            password='123456')

        self.team1 = create_team(
            name='teamname',
            introduction='testexample',
            creator=self.user1)

        self.user1.team = self.team1
        self.user1.save()

        self.user2.team = self.team1
        self.user2.save()

        self.room1 = create_room(
            name='roomname1',
            team=self.team1,
            creator=self.user1)
        self.room2 = create_room(
            name='roomname2',
            team=self.team1,
            creator=self.user2)

    def test_create_room(self):
        response_data = ResponseData()
        services.create_room(
            self.user1,
            'roomname3',
            response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        response_data = ResponseData()
        self.assertRaises(ValidationError,
                          services.create_room, self.user1,
                          'toooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolongnamemmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',
                          response_data)
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)

    def test_is_room_creator(self):
        response_data = ResponseData()
        self.assertRaises(MeetingRoom.DoesNotExist,
                          services.is_room_creator,
                          self.user1, not_exist_room_id,
                          response_data)
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)
        self.assertEqual(response_data.data, '当前会议室不存在')

        response_data = ResponseData()
        self.assertRaises(PermissionDenied,
                          services.is_room_creator,
                          self.user1, self.room2.id,
                          response_data)
        self.assertEqual(response_data.mt_status, MTStatus.FORBIDDEN)
        self.assertEqual(response_data.data, '当前用户不是会议室创建人')

        response_data = ResponseData()
        room = services.is_room_creator(
            self.user1, self.room1.id, response_data)
        self.assertEqual(self.room1, room)

    def test_is_room_exist(self):
        response_data = ResponseData()
        self.assertRaises(MeetingRoom.DoesNotExist,
                          services.is_room_exist,
                          not_exist_room_uuid,
                          response_data)
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)
        self.assertEqual(response_data.data, '当前会议室不存在')

        response_data = ResponseData()
        room = services.is_room_exist(self.room1.uuid, response_data)
        self.assertEqual(self.room1, room)

    def test_get_room_information(self):
        self.user3 = create_user(
            name='username3',
            email='test3@qq.com',
            password='123456')
        self.team2 = create_team(
            name='teamname2',
            introduction='testexample',
            creator=self.user3)
        self.user3.team = self.team2
        self.user3.save()
        self.room3 = create_room(
            name='roomname3',
            team=self.team2,
            creator=self.user3)

        response_data = ResponseData()
        self.assertRaises(PermissionDenied,
                          services.get_room_information, self.user1, self.room3, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.FORBIDDEN)

        response_data = ResponseData()
        services.get_room_information(self.user1, self.room1, response_data)
        self.assertEqual(response_data.data,
                         MeetingRoomSerializer(self.room1).data)


class TeamMemberTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user(
            name='username1',
            email='test1@qq.com',
            password='123456')
        self.user2 = create_user(
            name='username2',
            email='test2@qq.com',
            password='123456')

        self.team1 = create_team(
            name='teamname',
            introduction='testexample',
            creator=self.user1)

        self.user1.team = self.team1
        self.user1.save()

        self.user2.team = self.team1
        self.user2.save()

    def test_has_team(self):
        response_data = ResponseData()
        services.has_team(self.user1, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        response_data = ResponseData()
        self.user3 = create_user(
            name='username3',
            email='test3@qq.com',
            password='123456')
        self.assertRaises(Team.DoesNotExist, services.has_team,
                          self.user3, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.TEAM_NOT_EXIST)

    def test_get_team_members(self):
        response_data = ResponseData()
        services.get_team_members(self.team1, response_data)
        self.assertEqual(response_data.data, UserSerializerWithoutPassword(
            User.objects.filter(team_id=self.team1.id), many=True).data)

    def test_is_creator(self):
        response_data = ResponseData()
        services.is_creator(self.user1, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.OK)

        response_data = ResponseData()
        self.assertRaises(PermissionDenied, services.is_creator,
                          self.user2, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.FORBIDDEN)

    def test_belong_to_team(self):
        response_data = ResponseData()
        self.assertRaises(User.DoesNotExist, services.belong_to_team,
                          not_exist_user_id, self.team1, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.RECORD_NOT_FOUND)
        self.assertEqual(response_data.data, '当前用户不存在')

        response_data = ResponseData()
        self.user3 = create_user(
            name='username3',
            email='test3@qq.com',
            password='123456')
        self.assertRaises(PermissionDenied, services.belong_to_team,
                          self.user3.id, self.team1, response_data)
        self.assertEqual(response_data.mt_status, MTStatus.ERROR_INPUT)
        self.assertEqual(response_data.data, '当前用户不属于本团队')

        response_data = ResponseData()
        member = services.belong_to_team(
            self.user2.id, self.team1, response_data)
        self.assertEqual(member, self.user2)

    def test_delete_member(self):
        services.delete_member(self.user2)
        self.assertEqual(self.user2.team_id, None)
