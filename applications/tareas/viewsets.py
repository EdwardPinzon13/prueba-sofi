from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from applications.users.authenticationmixins import Authentication
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import Group,Permission


from .serializers import  ActivitySerializer,StateSerializer
from .models import Activity,State


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer



