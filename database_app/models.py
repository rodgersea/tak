from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from datetime import datetime, date


class Route(models.Model):
    route = models.CharField(max_length=50, unique=True)
    wall = models.CharField(max_length=50)
    crag = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    area = models.CharField(max_length=50)

    def __str__(self):
        return self.route

    def get_absolute_url(self):
        return reverse('route', args=[str(self.id)])


class SavedClimb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.route)


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    session = models.IntegerField()
    attempt = models.IntegerField()
    date = models.DateField(null=True)
    notes = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.route}, session: {self.session}, attempt: {self.attempt}'

