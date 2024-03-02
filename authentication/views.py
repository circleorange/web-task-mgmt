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

        print(f"signin.POST: {request.POST}")

        if form.is_valid():
            print("signin.POST.success")

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            user = authenticate(username = email, password = password)

            if user is not None:
                login(request, user)

                response = HttpResponse(status = 302)
                response["HX-Redirect"] = "/dashboard"
                return response
        else:
            print(f"signin.POST.fail: {form.errors}")
            form.add_error(None, "Email or Password are incorrect")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/login.html", {"form": form})

def signup(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

    if request.method == "POST":
        print(f"signup.POST.raw: {request.POST}")

        form = CustomUserCreationForm(request.POST)

        print(f"signup.POST: {form}")

        # Successful user registration process
        if form.is_valid():
            print("signup.POST.success")
            
            login(request, form.save())
            
            response = HttpResponse(status=302)
            response["HX-Redirect"] = "/dashboard"
            return response
        # Handling invalid form
        else:
            print(f"signup.POST.fail: {form.errors}")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

