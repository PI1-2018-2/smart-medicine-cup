from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact')
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=30)

class Cup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cup')
    cup_id = models.CharField(max_length=30)

class Record(models.Model):
    cup_id = models.CharField(max_length=30)
    PARTITION_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
    )
    
    event = models.CharField(max_length=100)
    moment = models.DateTimeField()
    partition = models.IntegerField(choices=PARTITION_CHOICES)