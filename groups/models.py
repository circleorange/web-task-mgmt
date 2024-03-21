from django.db import models

class Group(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(blank = True)

# removed temorarily as was causing issue with migrations in Django
"""
    users = models.ManyToManyField(
        "users.CustomUser", 
        through = "core.Belongs"
    )
"""