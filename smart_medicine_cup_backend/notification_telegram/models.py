from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
        return '%s %s' % (self.title, self.body)