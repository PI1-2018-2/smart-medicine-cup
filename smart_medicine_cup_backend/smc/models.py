from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Cup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = ArrayField(models.CharField(max_length=200))

    def __str__(self):
        return self.user.name


class Partition(models.Model):
    #  explicitly define id so we can return it in __str__
    id = models.AutoField(primary_key=True)
    cup = models.ForeignKey(Cup, on_delete=models.CASCADE)
    medicine_time = models.TimeField()
    medicine_date = models.DateTimeField()
    was_taken = models.BooleanField()

    def __str__(self):
        return "{} {}".format(medicine_date, medicine_time)
