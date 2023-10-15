from django.db import models


# Create your models here.
class Orbit(models.Model):
    JCAT = models.CharField(max_length=50, primary_key=True)
    OpOrbitOQU = models.CharField(max_length=100)
    inclination = models.FloatField()
    perigee = models.IntegerField()
    apogee = models.IntegerField()
    primary_planet = models.CharField(max_length=50)


class Satellites(models.Model):
    JCAT = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    piece = models.CharField(max_length=50)
    PL_name = models.CharField(max_length=50)
    parent = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    bus = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    altname = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)


class Dates(models.Model):
    JCAT = models.CharField(max_length=50, primary_key=True)
    Ldate = models.DateTimeField()
    Sdate = models.DateTimeField()
    Ddate = models.DateTimeField()
    Odate = models.DateTimeField()


class Specs(models.Model):
    JCAT = models.CharField(max_length=50, primary_key=True)
    motor = models.CharField(max_length=100)
    length = models.FloatField()
    diameter = models.FloatField()
    mass = models.IntegerField()
    drymass = models.IntegerField()
    tot_mass = models.IntegerField()
    span = models.FloatField()
    shape = models.CharField(max_length=50)

