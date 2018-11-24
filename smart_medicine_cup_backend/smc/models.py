from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"Name: {self.name} Phone: {self.phone}"


class Cup(models.Model):
    user = models.ManyToManyField(User)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)


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
    # Duration
    duration = models.IntegerField()

    def __str__(self):
        return f"Start time {self.start_time}, Period {self.period} for {self.duration} day(s)"


class Record(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE)
    cup = models.ForeignKey("Cup", on_delete=models.CASCADE)
    event = models.CharField(max_length=100)

    def __str__(self):
        return f"Alarm {self.alarm} from cup {self.cup}, event: {self.event}"
