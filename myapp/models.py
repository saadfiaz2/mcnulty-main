from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Reason(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class PhoneNumber(models.Model):
    number = models.CharField(max_length=15)  # Ensure uniqueness
    def __str__(self):
        return f"{self.number}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)

    def __str__(self):
        return self.user.username

# ✅ Signal to delete User when an Agent is deleted
@receiver(post_delete, sender=Agent)
def delete_associated_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
    
class Record(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)  # Set blank and null to True for manual editing
    time = models.DateTimeField(auto_now_add=True, null=True)
    delay = models.IntegerField()  # Assuming 'delay' is in seconds
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)

    def __str__(self):
        return f"Record {self.id}"