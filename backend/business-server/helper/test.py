from team.models import Application, MeetingRoom, Team
from user.models import User


def create_user(name, email, password):
    user = User(name=name, email=email, password=password)
    user.set_password(user.password)
    user.save()
    return user


def create_team(name, introduction, creator):
    team = Team(name=name, introduction=introduction, creator=creator)
    team.save()
    return team


def create_room(name, team, creator):
    room = MeetingRoom(name=name, team=team, creator=creator)
    room.save()
    return room


def create_application(user, team):
    application = Application(user=user, team=team)
    application.save()
    return application
