from django.db import models


class CovidData(models.Model):
    Country = models.CharField(max_length=255)
    SNo = models.PositiveIntegerField(primary_key=True)
    ObservationDate = models.DateField()
    Province_State = models.CharField(max_length=255, blank=True, null=True)
    LastUpdate = models.DateTimeField()
    Confirmed = models.FloatField()
    Deaths = models.FloatField()
    Recovered = models.FloatField()
    ISO3166_CountryCode = models.CharField(max_length=2, blank=True, null=True)
    Latitude = models.FloatField(blank=True, null=True)
    Longitude = models.FloatField(blank=True, null=True)
    coordinates = models.CharField(max_length=255, blank=True, null=True)
    mercator_x = models.FloatField(blank=True, null=True)
    mercator_y = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.Country} - {self.ObservationDate}"
