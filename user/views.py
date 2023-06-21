from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from state.models import STATE
from .models import *
from .serializers import *


class UserReName(APIView):
    serializers = USERRenameSerializers

    def post(self, request, pk):
        string = str(pk) + "@gsm.hs.kr"
        user = USER.objects.get(email=string)
        serializer = USERRenameSerializers(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            state = STATE()
            state.user = user
            string2 = str(int(pk / 1000)) + "-" + str(int(int(pk / 100) % 10))
            state.where = string2
            state.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
