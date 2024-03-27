from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    """
    Task Model with fields for title, label, description, status, and creator
    """
    # Model Foreign Keys
    user = models.ForeignKey('users.CustomUser', on_delete = models.CASCADE, null = True)
    group = models.ForeignKey('groups.Group', related_name = 'tasks', on_delete = models.CASCADE, null = True)
    template = models.ForeignKey('task_templates.TaskTemplate', on_delete = models.CASCADE, related_name = 'tasks')

    class Label(models.TextChoices):
        PERSONAL = "Personal", "Personal"
        FAMILY = "Family", "Family"
        WORK = "Work", "Work"
        ACADEMIC = "Academic", "Academic"
        OTHER = "Other", "Other"

    class Status(models.TextChoices):
        TODO = "To Do"
        IN_PROGRESS = "In Progress"
        COMPLETED = "Completed"

    class Priority(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"
    
    class Effort(models.TextChoices):
        LOW = "Low"
        MEDIUM = "Medium"
        HIGH = "High"

   # Model Fields
    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    start_date = models.DateField(null = True, blank = True)
    end_date = models.DateField(null = True, blank = True)
    label = models.CharField(max_length = 50, null = True, choices = Label.choices, default = Label.PERSONAL)
    status = models.CharField(max_length = 12, choices = Status.choices, default = Status.TODO)
    priority = models.CharField(max_length = 6, choices = Priority.choices, default = Priority.LOW, null = True)
    effort = models.CharField(max_length = 6, choices = Effort.choices, default = Effort.LOW, null = True)

    def __str__(self):
        return f"{self.pk}: {self.title}"
