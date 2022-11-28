from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from datetime import datetime, date
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class Route(models.Model):
    route = models.CharField(max_length=50,
                             unique=True)
    wall = models.CharField(max_length=50)
    crag = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    area = models.CharField(max_length=50)

    def __str__(self):
        return self.route

    def get_absolute_url(self):
        return reverse('route',
                       args=[str(self.id)])


class SavedClimb(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    route = models.ForeignKey(Route,
                              on_delete=models.CASCADE)

    def __str__(self):
        return str(self.route)


class Attempt(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    route = models.ForeignKey(Route,
                              on_delete=models.CASCADE)
    session = models.IntegerField()
    attempt = models.IntegerField()
    date = models.DateField(null=True)
    notes = models.CharField(max_length=200,
                             null=True)

    def __str__(self):
        return f'{self.user}, {self.route}, session: {self.session}, attempt: {self.attempt}'
