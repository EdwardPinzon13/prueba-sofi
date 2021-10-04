from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from applications.users.authenticationmixins import Authentication
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import Group,Permission


from .serializers import  UserSerializer,GroupSerializer,permissionSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes=[IsAdminUser,]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes=[IsAdminUser,]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = permissionSerializer
    #authentication_classes = (TokenAuthentication,)
    permission_classes=[IsAdminUser,]