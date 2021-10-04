from rest_framework import serializers

from .models import Activity,State

class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = '__all__'

