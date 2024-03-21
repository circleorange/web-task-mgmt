from django.db import models

class TaskTemplate(models.Model):
    name = models.CharField(max_length = 100)

    user = models.ForeignKey(
        'users.CustomUser', 
        on_delete = models.CASCADE, 
    )

class TemplateField(models.Model):
    template = models.ForeignKey(TaskTemplate, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    is_included = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
