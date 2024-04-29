from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Application, MeetingRoom, MeetingRoomFiles, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'introduction')


class ApplicantSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(
        source='user.name')
    applicant_email = serializers.CharField(
        source='user.email')

    class Meta:
        model = Application
        fields = ('id', 'applicant_name', 'applicant_email')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'


class MeetingRoomFileSerializer(ModelSerializer):
    class Meta:
        model = MeetingRoomFiles
        fields = '__all__'
