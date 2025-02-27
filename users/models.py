from django.contrib.auth.models import AbstractUser
from django.db import models


class RFUser(AbstractUser):
    email = models.EmailField(unique=True)
    render_coin = models.IntegerField(default=0)

    def __str__(self):
        return self.username
