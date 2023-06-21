from rest_framework import serializers

from .models import *


class USERRenameSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['name', 'Class']
