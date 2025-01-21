from django.db import models
from django.contrib.auth.models import User


class Reason(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_phone_number = models.CharField(max_length=15, blank=True, null=True)     
    def __str__(self):
        return self.user.username
    
    
class Record(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)  # Set blank and null to True for manual editing
    # time = models.DateTimeField()
    delay = models.IntegerField()  # Assuming 'delay' is in seconds
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)

    def __str__(self):
        return f"Record {self.id}"