from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name
