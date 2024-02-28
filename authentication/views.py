from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def auth_view(request):
    return render(request, "auth_view.html")

def signin(request):
    if request.method == "GET":
        return render(request, "registration/login.html")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(f"signin.POST: {form}")

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/login.html", {"form": form})

def signup(request):
    if request.method == "GET":
        return render(request, "registration/signup.html")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(f"signup.POST: {form}")

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# Authenticate User Credentials
def authenticate(req):
    email = req.POST.get("email")
    print(f"authenticate().email.value: {email}")

    if email == "": 
        print(f"authenticate().email.invalid")

        ctx = { "email_err_msg": "Invalid Email" }

        return render(req, "authenticate.html", ctx)

    # HX-Redirect header required to get HTMX update whole page
    response = HttpResponse(status=302)
    response['HX-Redirect'] = "/dashboard"
    return response
