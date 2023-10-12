from django.db import models

class OfficeLocation(models.Model):
    name = models.CharField(max_length=200, unique=True)

class IPAddressRange(models.Model):
    office_location = models.ForeignKey(OfficeLocation, on_delete=models.CASCADE)
    ip_range = models.CharField(max_length=50)

