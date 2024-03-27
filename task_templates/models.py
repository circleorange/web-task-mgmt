from django.db import models

class TaskTemplate(models.Model):
    name = models.CharField(
        max_length = 255)

    user = models.ForeignKey(
        'users.CustomUser', 
        on_delete = models.CASCADE, 
        related_name = 'templates')


class TemplateField(models.Model):
    template = models.ForeignKey(
        TaskTemplate, 
        related_name = 'fields',
        on_delete=models.CASCADE)

    field_name = models.CharField(max_length = 255)
    is_enabled = models.BooleanField(default = True)
    is_required = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.field_name}: ({'required' if self.is_required else 'optional'})"
