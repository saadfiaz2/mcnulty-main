from rest_framework import serializers
from .models import Reason, Record, Agent

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone_numbers']
        

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ['id', 'title']

class RecordSerializer(serializers.ModelSerializer):
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all(), write_only=True)
    reason = serializers.PrimaryKeyRelatedField(queryset=Reason.objects.all(), write_only=True)

    class Meta:
        model = Record
        fields = ['id', 'agent', 'number', 'delay', 'reason', 'time'] 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)