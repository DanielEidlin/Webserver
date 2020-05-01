from .models import Attacker, Victim
from rest_framework import serializers
from django.contrib.auth.models import User


class AttackerSerializer(serializers.ModelSerializer):
    """
    Attacker serializer, responsible for converting the Attacker model to a serialized form that can be used in rest
    api.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Attacker
        # Fields to include in the api.
        fields = ['name', 'victim', 'owner', 'channel_name']


class VictimSerializer(serializers.ModelSerializer):
    """
    Victim serializer, responsible for converting the Victim model to a serialized form that can be used in rest api.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Victim
        # Fields to include in the api.
        fields = ['computer_name', 'mac_address', 'logged_in', 'owner', 'channel_name']


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer, responsible for converting the User model to a serialized form that can be used in rest api.
    """
    attacker = serializers.PrimaryKeyRelatedField(queryset=Attacker.objects.all(), allow_null=True)
    victim = serializers.PrimaryKeyRelatedField(queryset=Victim.objects.all(), allow_null=True)

    class Meta:
        model = User
        # Fields to include in the api.
        fields = ['id', 'username', 'attacker', 'victim']
