from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerWithoutPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
