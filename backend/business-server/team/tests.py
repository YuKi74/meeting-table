from constant.teamtest import not_exist_application_id, not_exist_team_uuid
from django.test import TestCase
from helper.test import create_application, create_team, create_user
from mt.errors import HasTeam
from mt.status import MTStatus
from mt.views import ResponseData
from rest_framework.exceptions import ValidationError
from team import services

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
            not_exist_team_uuid,
            response_data)
        self.assertEqual(response_data.mt_status, MTStatus.TEAM_NOT_EXIST)

        response_data = ResponseData()
        services.get_team_detail(self.team1.uuid, response_data)
        self.assertEqual(response_data.data,
                         TeamInformationSerializer(self.team1).data)
