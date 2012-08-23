from django.db import models

# Create your models here.

class Flight(models.Model):
    carrier = models.CharField(max_length=64)
    number = models.CharField(max_length=8)
    origin = models.CharField(max_length=64)
    arrives = models.DateTimeField()
    terminal = models.CharField(max_length=64)
    code_share = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return '<Flight: {}>'.format(self.number)

class Person(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=128, blank=True, null=True)
    twitter = models.CharField(max_length=64, blank=True, null=True)
    flight = models.ForeignKey(Flight)
    day = models.IntegerField(default=1)

    def __str__(self):
        return '<Person: {}>'.format(self.name)
