from django import forms
from .models import TaskTemplate, TemplateField
from task_templates.models import TemplateField


class TemplateFieldForm(forms.ModelForm):
    class Meta:
        model = TemplateField
        fields = ['field_name', 'is_required', 'is_included'] 


class TaskTemplateForm(forms.ModelForm):
    class Meta:
        model = TaskTemplate
        fields = ["name"]
