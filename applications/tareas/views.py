from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import ActivitySerializer
# Create your views here.

from .models import  *

class ActivityListAPIView(ListAPIView):
    model = Activity
    queryset = Activity.objects.get_activities_finished_bloked()
    serializer_class = ActivitySerializer


class ActivityToFinishListAPIView(ListAPIView):
    model = Activity
    queryset = Activity.objects.get_activities_to_finish()
    if queryset == []:
        print('vacio')

    serializer_class = ActivitySerializer





