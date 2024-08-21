from django.db import models
from django.utils import timezone

class Reading(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.temperature}°C, {self.humidity}%, {self.timestamp}"
