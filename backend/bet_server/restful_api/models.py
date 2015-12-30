from django.db import models


class Bet(models.Model):
    title = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    outcome = models.NullBooleanField(default=None)

    def __str__(self):
        return self.title
