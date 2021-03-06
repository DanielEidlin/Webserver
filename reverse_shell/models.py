from django.db import models
from django.contrib.auth.models import User


class Victim(models.Model):
    """
    This class represents a victim object.
    """
    mac_address = models.CharField(max_length=200, primary_key=True)
    computer_name = models.CharField(max_length=200, blank=True)
    logged_in = models.BooleanField(default=True)
    owner = models.OneToOneField(User, related_name='victim', on_delete=models.CASCADE)
    # The channel name of the websocket connected to the victim, if there is one.
    channel_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.computer_name


class Attacker(models.Model):
    """
    This class represents an attacker object.
    """
    name = models.CharField(max_length=200, blank=True, primary_key=True)
    victim = models.OneToOneField(Victim, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.OneToOneField(User, related_name='attacker', on_delete=models.CASCADE)
    # The channel name of the websocket connected to the victim, if there is one.
    channel_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.owner.username
        super().save(*args, **kwargs)
