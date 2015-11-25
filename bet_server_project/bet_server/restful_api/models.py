from django.db import models

# Create your models here.

class Bet(models.Model):        
    #    happened = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    def __str__(self):
        return self.title
