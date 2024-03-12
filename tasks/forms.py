from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "label",
            "description",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(attrs = { "class": "form-control" }),
            "label": forms.Select(attrs = { "class": "form-control" }),
            "description": forms.Textarea(attrs = { "class": "form-control", "rows": 3 }),
            "status": forms.Select(attrs = { "class": "form-control" }),
        }
