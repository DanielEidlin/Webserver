from django.db import models


class Victim(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField(blank=True, null=True)
    mac_address = models.CharField(max_length=200, unique=True, primary_key=True)
    computer_name = models.CharField(max_length=200, blank=True)
    logged_in = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.computer_name} {self.ip} {self.port}'


class Attacker(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    mac_address = models.CharField(max_length=200, unique=True, primary_key=True)
    computer_name = models.CharField(max_length=200, blank=True)
    victim = models.OneToOneField(Victim, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.computer_name} {self.ip} {self.port}'
