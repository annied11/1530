from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    category = models.CharField(max_length=100)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.name
