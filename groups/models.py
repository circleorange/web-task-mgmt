from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(blank = True)

    # model mapping
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "user_groups")