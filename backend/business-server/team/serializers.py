from rest_framework.serializers import ModelSerializer
from .models import MeetingRoom
from rest_framework import serializers

from .models import Application, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('name', 'introduction', 'creator')


class ApplicantSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(
        source='user.name')
    applicant_email = serializers.CharField(
        source='user.email')

    class Meta:
        model = Application
        fields = ('applicant_name', 'applicant_email')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class MeetingRoomSerializer(ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'
