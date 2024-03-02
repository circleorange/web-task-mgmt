from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate


# Custom Signup Form 
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit: user.save()

        return user

# Custom Signin Form
class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(required = True)
    password = forms.CharField(
            label = "Password", 
            strip = False, 
            widget = forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(self.request, username = email, password = password)

        if user is None:
            raise forms.ValidationError("Please enter correct email and password", code="invalid_login")

        # store authenticate user for future use if needed
        self.user_cache = user

        return cleaned_data
