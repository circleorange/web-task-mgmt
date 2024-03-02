from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def auth_view(request):
    return render(request, "auth_view.html")


def signin(request):
    if request.method == "GET":
        form = CustomAuthenticationForm()
        return render(request, "registration/login.html", {"form": form})

    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)

        print(f"siginin.POST.form: {form}")

        if form.is_valid():
            print("signin.POST.form.is_valid: true")

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username = email, password = password)

            # If user is valid, accept authentication and redirect user to dashboard
            if user is not None:
                login(request, user)

                response = HttpResponse(status = 302)
                response["HX-Redirect"] = "/dashboard"
                return response
        else:
            pass
            print("signin.POST.form.is_valid: false")
            # form.add_error(None, "Email or Password are incorrect")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/login.html", {"form": form})


def signup(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        print(f"signup.POST.form: {form}")

        # Successful user registration process
        if form.is_valid():
            print("signup.POST.form.is_valid: true")
            
            login(request, form.save())
            
            response = HttpResponse(status=302)
            response["HX-Redirect"] = "/dashboard"
            return response
        # Handling invalid form
        else:
            print(f"signup.POST.form.is_valid: false: {form.errors}")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

