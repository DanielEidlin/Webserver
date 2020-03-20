from .models import Attacker, Victim
from rest_framework import serializers
from django.contrib.auth.models import User


class AttackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attacker
        fields = ['ip', 'port', 'computer_name', 'mac_address', 'victim', 'owner']


class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = ['ip', 'port', 'computer_name', 'mac_address', 'logged_in', 'owner']


class UserSerializer(serializers.ModelSerializer):
    attacker = serializers.PrimaryKeyRelatedField(queryset=Attacker.objects.all(), allow_null=True)
    victim = serializers.PrimaryKeyRelatedField(queryset=Victim.objects.all(), allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'attacker', 'victim']
