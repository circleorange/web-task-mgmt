from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    """
    Task Model with fields for title, label, description, status, and creator
    """

    class Label(models.TextChoices):
        PERSONAL = "Personal", "Personal"
        FAMILY = "Family", "Family"
        WORK = "Work", "Work"
        ACADEMIC = "Academic", "Academic"

    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
    
    title = models.CharField(max_length = 255)
    label = models.CharField(
        max_length = 50, 
        choices = Label.choices, 
        default = Label.PERSONAL
    )
    description = models.TextField(blank = True)
    status = models.CharField(
        max_length = 12,
        choices = Status.choices,
        default = Status.TODO
    )
    creator = models.ForeignKey(
        User, 
        on_delete = models.CASCADE, 
        related_name = "tasks"
    )
