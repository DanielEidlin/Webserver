from .models import Attacker, Victim
from rest_framework import serializers
from django.contrib.auth.models import User


class AttackerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Attacker
        fields = ['name', 'victim', 'owner', 'channel_name']


class VictimSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Victim
        fields = ['computer_name', 'mac_address', 'logged_in', 'owner', 'channel_name']


class UserSerializer(serializers.ModelSerializer):
    attacker = serializers.PrimaryKeyRelatedField(queryset=Attacker.objects.all(), allow_null=True)
    victim = serializers.PrimaryKeyRelatedField(queryset=Victim.objects.all(), allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'attacker', 'victim']
