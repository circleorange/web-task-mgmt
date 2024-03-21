from django.db import models

class Belongs(models.Model):
    """
    Class enabling the mapping of ManyToMany relationship of User and Group models
    """
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete = models.CASCADE,
        null = True
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete = models.CASCADE,
        null = True
    )

    class Role(models.TextChoices):
        LEADER = "Leader"
        MEMBER = "Member"

    role = models.CharField(
        max_length = 10,
        choices = Role.choices,
        default = Role.MEMBER
    )

    class Meta:
        # ensure unique membership
        unique_together = ("user", "group")