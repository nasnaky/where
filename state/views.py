from django.utils.datetime_safe import date
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import APIView
from django.utils import timezone

from .serializers import *


def verify_jwt(token):
    try:
        JWTAuthentication().get_validated_token(token)
        return True
    except InvalidToken:
        return False


class QRChange(APIView):
    serializer_class = ChangeSerializers

    def post(self, request):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = ChangeSerializers(data=request.data)
            if serializer.is_valid():
                try:
                    state = STATE.objects.get(Q(user=user) & Q(date=timezone.now().date()))
                    wheres = serializer.validated_data.get('where')
                    state.where = wheres
                    state.save()
                except Exception:
                    serializer.save(user=user)
                return Response({
                    "message": "현재 위치가 변경됐습니다."
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "잘못된 요청입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class TeaChange(APIView):
    serializer_class = ChangeSerializers

    def post(self, request, pk):
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        if verify_jwt(accessToken):
            decoded_token = AccessToken(accessToken)
            decoded_payload = decoded_token.payload
            user = USER.objects.get(pk=decoded_payload["user_id"])
            serializer = ChangeSerializers(data=request.data)
            if user.T_bool:
                if serializer.is_valid():
                    C_user = USER.objects.get(Class=pk)
                    try:
                        state = STATE.objects.get(Q(user=C_user) & Q(date=timezone.now().date()))
                        wheres = serializer.validated_data.get('where')
                        state.where = wheres
                        state.save()
                    except Exception:
                        serializer.save(user=C_user)
                    return Response({
                        "message": "현재 위치가 변경됐습니다."
                    }, status=status.HTTP_200_OK)
                return Response({
                    "message": "잘못된 요청입니다."
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "message": "선생님이 아닙니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "유효하지 않은 토큰입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


class List(APIView):
    def get(self, request):
        user_list = USER.objects.filter(Q(is_superuser=False) & Q(T_bool=False))

        try:
            grade = request.query_params['grade']
            grade = int(grade) * 1000
            grade_user = USER.objects.filter(Q(Class__gte=grade) & Q(Class__lte=grade + 999))
            user_list = user_list.intersection(grade_user)
        except Exception:
            pass

        try:
            group = request.query_params['group']
            group = int(group)
            group_user = USER.objects.filter(Class__regex=r'^\d' + str(group) + '\d{2}$')
            user_list = user_list.intersection(group_user)
        except Exception:
            pass

        try:
            name = request.query_params['name']
            name_user = USER.objects.filter(name__contains=name)
            user_list = user_list.intersection(name_user)
        except Exception:
            pass

        try:
            states = request.query_params['state']
            check = 1
        except Exception:
            check = 0

        serializer = []

        for user in user_list.order_by('id'):
            try:
                state = STATE.objects.get(Q(user=user) & Q(date=date.today()))
            except Exception:
                state = STATE.objects.filter(user=user).order_by('id')[0]
            if check:
                if state.where == states:
                    serializer.append(state)
            else:
                serializer.append(state)

        serializer = ListSerializers(serializer, many=True)
        return Response(serializer.data)
