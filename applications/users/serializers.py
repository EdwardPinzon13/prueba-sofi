from rest_framework import serializers
from django.contrib.auth.models import Group,Permission
from .models import User


class permissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('__all__')
        
class GroupSerializer(serializers.ModelSerializer):
    permissions = permissionSerializer(many=True)
    class Meta:
        model = Group
        fields = ('__all__')

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        update_user = super().update(instance, validated_data)
        update_user.set_password(validated_data['password'])
        update_user.save()
        return  update_user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id':instance['id'],
            'username':instance['username'],
            'email':instance['email'],
            'password':instance['password'],
        }

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=(
            'username',
            'email',
            'name',
            'last_name'
        )
