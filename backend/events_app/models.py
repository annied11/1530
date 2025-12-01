from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="events",
    )

    location = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField()
    category = models.CharField(max_length=100, blank=True)

    external_id = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.name
