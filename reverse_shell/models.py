from django.db import models
from django.contrib.auth.models import User


class Victim(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField(blank=True, null=True)
    mac_address = models.CharField(max_length=200, unique=True, primary_key=True)
    computer_name = models.CharField(max_length=200, blank=True)
    logged_in = models.BooleanField(default=True)
    owner = models.OneToOneField(User, related_name='victim', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.computer_name} {self.ip} {self.port}'


class Attacker(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    mac_address = models.CharField(max_length=200, unique=True, primary_key=True)
    computer_name = models.CharField(max_length=200, blank=True)
    victim = models.OneToOneField(Victim, on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.OneToOneField(User, related_name='attacker', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.computer_name} {self.ip} {self.port}'
