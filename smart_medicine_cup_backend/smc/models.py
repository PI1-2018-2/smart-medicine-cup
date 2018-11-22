from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Cup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = ArrayField(models.CharField(max_length=200))

    def __str__(self):
        return self.user.name


class Partition(models.Model):
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE)
    was_taken = models.BooleanField()
    message_moment = models.TimeField()

    def __str__(self):
        return self.id


class Alarm(models.Model):
    partition = models.ForeignKey(Partition, on_delete=models.CASCADE)
    start_time = models.TimeField()
    period = models.TimeField()
    # Duration
    day_length = models.IntegerField()
    # Registered or cancelled
    event = models.CharField(max_length=50)

    def __str__(self):
        return f"Start time {self.start_time}, Period {self.period} for {self.day_length} day(s)"