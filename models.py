
from django.db import models
from django.contrib.auth.models import User


class SeamUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kid = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.kid

