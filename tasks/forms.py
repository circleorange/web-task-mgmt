from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['user', 'template'] # user and template are set in the view


    def __init__(self, *args, template=None, **kwargs):
            super().__init__(*args, **kwargs)
            
            if template:
                # Initialize the form with fields based on the template
                for field in template.template_fields.all():
                    if field.is_enabled:
                        if field.field_name == 'title':
                            self.fields['title'].required = field.is_required
                        elif field.field_name == 'description':
                            self.fields['description'].required = field.is_required
                        # Add similar blocks for other fields based on your model
                        
                # Disable fields not included in the template
                for field_name in self.fields:
                    if not template.template_fields.filter(field_name=field_name, is_enabled=True).exists():
                        del self.fields[field_name]