from django.db import models

# Create your models here.

class WeatherData(models.Model):
    date = models.DateField()
    temp = models.FloatField()
    mintemp = models.FloatField()
    maxtemp = models.FloatField()
    pressure = models.FloatField()
    precipation = models.FloatField()
    wind = models.IntegerField()
    winddir = models.CharField(max_length=7)
    sunshine = models.FloatField()
    dewpoint = models.FloatField()



