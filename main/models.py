from django.db import models


class Weather(models.Model):
    name = models.CharField('Name', max_length=30)
    country = models.CharField('Country ISO', max_length=8)
    dat = models.DateTimeField('Date and time')
    icon = models.CharField('Icon', max_length=10, default='04d')
    wind = models.FloatField('Wind speed')
    visibility = models.IntegerField('Visibility')
    temp = models.FloatField('Temperature')
    feels_like = models.FloatField('Feels like')
    humidity = models.IntegerField('Humidity')
    pressure = models.IntegerField('Pressure')

    def __str__(self):
        return self.name