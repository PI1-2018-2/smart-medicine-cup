from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, default='00000000')
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return f"Name: {self.name} Phone: {self.phone}"


class Cup(models.Model):
    cup_id = models.CharField(max_length=200, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class Alarm(models.Model):
    PARTITION_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
    )

    cup = models.ForeignKey(Cup, on_delete=models.CASCADE)
    partition = models.IntegerField(choices=PARTITION_CHOICES)
    start_time = models.TimeField()
    period = models.TimeField()
    duration = models.IntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.is_active} - Start time {self.start_time}, Period {self.period} for {self.duration} day(s)"


class Record(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    moment = models.DateTimeField()

    def __str__(self):
        return f"[{self.moment}]: Alarm {self.alarm} {self.event}"
