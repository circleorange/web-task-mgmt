from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Custom Sign Up Form 
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 30, required = True)
    last_name = forms.CharField(max_length = 30, required = True)
    email = forms.EmailField(max_length = 254, help_text="Enter valid email address")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")


# Custom Sign In Form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label = "Email",
        widget = forms.TextInput(attrs = { "autofocus": True })
    )

    def clean(self):
        print("CustomAuthenticationForm.clean.start")
        cleaned_data = super().clean()
        email = cleaned_data.get("username")
        cleaned_data["username"] = User.objects.normalize_email(email)

        return cleaned_data
