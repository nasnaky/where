from django.urls import path, include

from .views import *

urlpatterns = [
    path('', QRChange.as_view()),
    path('<int:pk>', TeaChange.as_view()),
    path('list/', List.as_view())
]
