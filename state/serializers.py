from rest_framework import serializers

from .models import *
from user.models import USER


class ChangeSerializers(serializers.ModelSerializer):
    class Meta:
        model = STATE
        fields = ['where']


class UserListSerializers(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = ['name', 'grade', 'group', 'number']

    def get_grade(self, obj):
        if isinstance(obj, USER):
            string = obj.Class
            return str(int(string / 1000))
        return None

    def get_group(self, obj):
        if isinstance(obj, USER):
            string = obj.Class
            return str(int(int(string / 1000) % 10))
        return None

    def get_number(self, obj):
        if isinstance(obj, USER):
            string = obj.Class
            return str(int(string % 100))
        return None


class ListSerializers(serializers.ModelSerializer):
    user = UserListSerializers()

    class Meta:
        model = STATE
        fields = ['user', 'where']

